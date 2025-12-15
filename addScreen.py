# addScreen.py
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox


class AddScreen:
    def __init__(self, root, app, on_saved, entry=None):
        """
        root: main Tk root (used as parent)
        app: PasswordManager instance (for db, crypto, current user)
        on_saved: callback to refresh vault entries after successful add
        """
        self.window = None
        self.app = app
        self.on_saved = on_saved
        self.entry=entry

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

        button_text = "Save" if self.entry else "Add"
        add_button = ttk.Button(self.addScreen, text=button_text, command=self.save_click)
        add_button.grid(column=1, row=4, pady=(5, 15), sticky="e")

        if self.entry:
            self.site_entry.insert(0, self.entry["site"])
            self.username_entry.insert(0, self.entry["username"])
            self.password_entry.insert(0, self.entry["password"])
            self.notes_text.insert("1.0", self.entry["notes"])
        self.site_entry.focus()

    def save_click(self):
        site = self.site_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        notes = self.notes_text.get("1.0", "end").strip()

        if not site or not username or not password:
            messagebox.showerror(
                "Missing Data", "Site, username, and password are required."
            )
            return


        if self.entry:
            self.app.db.update_entry(
                entry_id=self.entry["id"],
                key=self.app.current_key,
                crypto=self.app.crypto,
                site=site,
                username=username,
                password=password,
                notes=notes,
            )
        else:
            self.app.db.add_entry(
                self.app.current_user_id,
                self.app.current_key,
                self.app.crypto,
                site,
                username,
                password,
                notes,
            )

        self.on_saved()
        self.addScreen.destroy()
