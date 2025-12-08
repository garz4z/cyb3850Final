# vaultScreen.py
import tkinter as tk
from tkinter import ttk

from addScreen import AddScreen


class VaultScreen:
    def __init__(self, root, app):
        """
        root: main Tk root
        app: PasswordManager instance (holds current_user_id, db, crypto)
        """
        self.root = root
        self.app = app

        self.root.title("Password Manager - Vault")

        self._build_ui()
        self._populate_table()

    def _build_ui(self):
        # Header row
        header_frame = ttk.Frame(self.root)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5, padx=10)

        vault_label = ttk.Label(
            header_frame,
            text=f"{self.app.current_username}'s Vault"
            if self.app.current_username
            else "User's Vault",
        )
        vault_label.configure(font=("Arial", 14, "bold"))
        vault_label.pack(side="left")

        add_button = ttk.Button(
            header_frame, text="Add New Password", command=self.add_password_click
        )
        add_button.pack(side="right", padx=(0, 5))

        signout_button = ttk.Button(
            header_frame, text="Sign Out", command=self.signout_click
        )
        signout_button.pack(side="right", padx=(0, 10))

        # Table frame
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        frame = ttk.Frame(self.root)
        frame.grid(column=0, row=1, columnspan=2, padx=10, pady=5, sticky="nsew")

        columns = ("Site", "Username", "Password", "Date Added")
        self.table = ttk.Treeview(frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.table.heading(col, text=col)

        self.table.column("Site", stretch=tk.YES, width=200)
        self.table.column("Username", stretch=tk.YES, width=200)
        self.table.column("Password", stretch=tk.YES, width=200)
        self.table.column("Date Added", width=120, stretch=tk.NO)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        self.table.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    def _populate_table(self):
        """Load entries from the DB for current user and insert into table."""
        # Clear existing rows
        for item in self.table.get_children():
            self.table.delete(item)

        if self.app.current_user_id is None or self.app.current_key is None:
            return

        entries = self.app.db.get_entries_for_user(
            self.app.current_user_id, self.app.current_key, self.app.crypto
        )

        for entry in entries:
            self.table.insert(
                "",
                "end",
                values=(
                    entry["site"],
                    entry["username"],
                    entry["password"],
                    entry["created_at"],
                ),
            )

    # ---------- Buttons ----------

    def signout_click(self):
        self.app.sign_out()

    def add_password_click(self):
        # Open AddScreen and refresh table after it closes
        AddScreen(self.root, app=self.app, on_saved=self._populate_table)
