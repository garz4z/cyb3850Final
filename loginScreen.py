# loginScreen.py
import tkinter as tk
from tkinter import ttk, messagebox


class LoginScreen:
    def __init__(self, root, app):
        """
        root: main Tk root
        app: PasswordManager instance (provides db/crypto + navigation)
        """
        self.root = root
        self.app = app

        self.root.title("Login - Password Manager")
        self.root.geometry("500x300")
        self.root.resizable(False, False)

        self._build_ui()

    def _build_ui(self):
        # Title
        title_label = ttk.Label(self.root, text="Password Manager Login")
        title_label.configure(font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 10))

        # Username / password fields
        ttk.Label(self.root, text="Username: ").grid(
            row=1, column=0, padx=(60, 10), pady=(20, 5), sticky="e"
        )
        self.username_entry = ttk.Entry(self.root, width=40)
        self.username_entry.grid(row=1, column=1, pady=(20, 5), sticky="w")

        ttk.Label(self.root, text="Password: ").grid(
            row=2, column=0, padx=(60, 10), pady=(5, 5), sticky="e"
        )
        self.password_entry = ttk.Entry(self.root, width=40, show="*")
        self.password_entry.grid(row=2, column=1, pady=(5, 5), sticky="w")

        self.username_entry.focus()

        # Buttons
        login_button = ttk.Button(self.root, text="Log In", command=self.login_click)
        create_button = ttk.Button(
            self.root, text="Create Account", command=self.create_user_click
        )

        login_button.grid(row=3, column=1, pady=(15, 5), sticky="w")
        create_button.grid(row=4, column=1, pady=(5, 5), sticky="w")

    # ---------- Button handlers ----------

    def login_click(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        success, msg = self.app.attempt_login(username, password)
        if not success:
            messagebox.showerror("Login Failed", msg)
            return

        # Success: go to vault
        self.app.show_vault()

    def create_user_click(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()

        success, msg = self.app.create_user(username, password)
        if success:
            messagebox.showinfo("User Created", msg)
        else:
            messagebox.showerror("Error", msg)
