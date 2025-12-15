# addScreen.py
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox


class AddScreen:
    def __init__(self, root, app, on_saved):
        """
        root: main Tk root (used as parent)
        app: PasswordManager instance (for db, crypto, current user)
        on_saved: callback to refresh vault entries after successful add
        """
        self.app = app
        self.on_saved = on_saved

        self.addScreen = tk.Toplevel(root)
        self.addScreen.title("Add Password")
        self.addScreen.resizable(True, True)
        self.addScreen.minsize(400, 300)

        self._build_ui()

    def _build_ui(self):
        pad_x = (30, 10)

        ttk.Label(self.addScreen, text="Site / Service:").grid(
            row=0, column=0, padx=pad_x, pady=(20, 5), sticky="e"
        )
        self.site_entry = ttk.Entry(self.addScreen, width=40)
        self.site_entry.grid(row=0, column=1, pady=(20, 5), sticky="w")

        ttk.Label(self.addScreen, text="Username / Email:").grid(
            row=1, column=0, padx=pad_x, pady=(5, 5), sticky="e"
        )
        self.username_entry = ttk.Entry(self.addScreen, width=40)
        self.username_entry.grid(row=1, column=1, pady=(5, 5), sticky="w")

        ttk.Label(self.addScreen, text="Password:").grid(
            row=2, column=0, padx=pad_x, pady=(5, 5), sticky="e"
        )
        self.password_entry = ttk.Entry(self.addScreen, width=40, show="*")
        self.password_entry.grid(row=2, column=1, pady=(5, 5), sticky="w")

        ttk.Label(self.addScreen, text="Notes (optional):").grid(
            row=3, column=0, padx=pad_x, pady=(5, 5), sticky="ne"
        )
        self.notes_text = tk.Text(self.addScreen, width=30, height=4)
        self.notes_text.grid(row=3, column=1, pady=(5, 10), sticky="w")

        add_button = ttk.Button(self.addScreen, text="Add", command=self.add_click)
        add_button.grid(column=1, row=4, pady=(5, 15), sticky="e")

        self.site_entry.focus()

    def add_click(self):
        site = self.site_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        notes = self.notes_text.get("1.0", tk.END).strip()

        if not site or not username or not password:
            messagebox.showerror(
                "Missing Data", "Site, username, and password are required."
            )
            return

        if self.app.current_user_id is None or self.app.current_key is None:
            messagebox.showerror("Error", "No user logged in.")
            return

        try:
            self.app.db.add_entry(
                user_id=self.app.current_user_id,
                key=self.app.current_key,
                crypto=self.app.crypto,
                site=site,
                username=username,
                password=password,
                notes=notes,
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add entry: {e}")
            return

        # Refresh table in vault and close
        if self.on_saved:
            self.on_saved()
        self.addScreen.destroy()
