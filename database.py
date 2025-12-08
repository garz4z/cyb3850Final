# database.py
from __future__ import annotations

import os
import sqlite3
from datetime import datetime
import json

from crypto_service import CryptoService


class VaultDB:
    def __init__(self, db_path: str = "vault.db"):
        self.db_path = db_path
        # Ensure directory exists if db_path includes dirs
        os.makedirs(os.path.dirname(db_path), exist_ok=True) if os.path.dirname(db_path) else None

        self.conn = sqlite3.connect(self.db_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self._create_tables()

    def _create_tables(self):
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE NOT NULL,
                    salt BLOB NOT NULL,
                    iterations INTEGER NOT NULL,
                    check_nonce BLOB NOT NULL,
                    check_cipher BLOB NOT NULL,
                    check_tag BLOB NOT NULL
                );
                """
            )
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS entries (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    site TEXT NOT NULL,
                    data_nonce BLOB NOT NULL,
                    data_cipher BLOB NOT NULL,
                    data_tag BLOB NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );
                """
            )

    # ---------- Users ----------

    def create_user(self, username: str, master_password: str, crypto: CryptoService) -> int:
        """Create a new user with username + master password. Returns user_id."""
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cur.fetchone() is not None:
            raise ValueError("Username already exists")

        salt = os.urandom(16)
        key = crypto.derive_key(master_password, salt)
        nonce, cipher, tag = crypto.encrypt("vault-check", key)
        iterations = crypto.iterations

        with self.conn:
            cur = self.conn.execute(
                """
                INSERT INTO users (username, salt, iterations, check_nonce, check_cipher, check_tag)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (username, salt, iterations, nonce, cipher, tag),
            )

        return cur.lastrowid

    def verify_login(self, username: str, master_password: str, crypto: CryptoService):
        """
        Verify username + master password.
        Returns (user_id, key) on success, or (None, None) on failure.
        """
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT id, salt, iterations, check_nonce, check_cipher, check_tag
            FROM users
            WHERE username = ?
            """,
            (username,),
        )
        row = cur.fetchone()
        if row is None:
            return None, None

        user_id, salt, iterations, nonce, cipher, tag = row
        key = crypto.derive_key(master_password, salt, iterations)

        try:
            plaintext = crypto.decrypt(nonce, cipher, tag, key)
        except Exception:
            return None, None

        if plaintext != "vault-check":
            return None, None

        return user_id, key

    # ---------- Entries ----------

    def add_entry(
        self,
        user_id: int,
        key: bytes,
        crypto: CryptoService,
        site: str,
        username: str,
        password: str,
        notes: str | None = None,
    ):
        """Add encrypted entry for a user."""
        if notes is None:
            notes = ""

        data_obj = {
            "username": username,
            "password": password,
            "notes": notes,
        }
        data_json = json.dumps(data_obj)
        nonce, cipher, tag = crypto.encrypt(data_json, key)
        now = datetime.utcnow().isoformat(timespec="seconds")

        with self.conn:
            self.conn.execute(
                """
                INSERT INTO entries (user_id, site, data_nonce, data_cipher, data_tag, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (user_id, site, nonce, cipher, tag, now, now),
            )

    def get_entries_for_user(self, user_id: int, key: bytes, crypto: CryptoService):
        """Return a list of decrypted entries for a user."""
        cur = self.conn.cursor()
        cur.execute(
            """
            SELECT id, site, data_nonce, data_cipher, data_tag, created_at, updated_at
            FROM entries
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (user_id,),
        )

        entries = []
        for row in cur.fetchall():
            entry_id, site, nonce, cipher, tag, created_at, updated_at = row
            try:
                data_json = crypto.decrypt(nonce, cipher, tag, key)
                data_obj = json.loads(data_json)
            except Exception:
                # In case of corruption, skip this entry
                continue

            entries.append(
                {
                    "id": entry_id,
                    "site": site,
                    "username": data_obj.get("username", ""),
                    "password": data_obj.get("password", ""),
                    "notes": data_obj.get("notes", ""),
                    "created_at": created_at,
                    "updated_at": updated_at,
                }
            )
        return entries
