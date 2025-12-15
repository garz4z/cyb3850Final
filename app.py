# app.py
import tkinter as tk

from loginScreen import LoginScreen
from vaultScreen import VaultScreen
from database import VaultDB
from crypto_service import CryptoService


class PasswordManager:
    def __init__(self):
        # Core app state
        self.db = VaultDB("vault.db")
        self.crypto = CryptoService()
        self.current_user_id = None
        self.current_key = None
        self.current_username = None

        # Single Tk root
        self.root = tk.Tk()
        self.root.title("Lock It Down Password Manager")
        self.root.state("zoomed")
        self.root.resizable(True, True)

        self.show_login()

    # ---------- Screen Management ----------

    def clear_root(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear_root()
        LoginScreen(self.root, app=self)

    def show_vault(self):
        self.clear_root()
        VaultScreen(self.root, app=self)

    def sign_out(self):
        self.current_user_id = None
        self.current_key = None
        self.current_username = None
        self.show_login()

    # ---------- Auth / DB hooks ----------

    def create_user(self, username: str, master_password: str) -> tuple[bool, str]:
        """Create account, returning (success, message)."""
        if not username or not master_password:
            return False, "Username and password cannot be empty."

        try:
            self.db.create_user(username, master_password, self.crypto)
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Failed to create user: {e}"
        return True, "User created successfully."

    def attempt_login(self, username: str, master_password: str) -> tuple[bool, str]:
        """Attempt login, returning (success, message)."""
        if not username or not master_password:
            return False, "Username and password cannot be empty."

        user_id, key = self.db.verify_login(username, master_password, self.crypto)
        if user_id is None or key is None:
            return False, "Invalid username or password."

        self.current_user_id = user_id
        self.current_key = key
        self.current_username = username
        return True, "Login successful."

    def run(self):
        self.root.mainloop()
