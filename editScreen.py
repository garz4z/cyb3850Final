# editScreen.py
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox


class EditScreen:
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

        self.editScreen = tk.Toplevel(root)
        self.editScreen.title("Edit Password")
        self.editScreen.resizable(False, False)
        self.editScreen.geometry("400x300")
        self.editScreen.configure(background="grey74")

        self._build_ui()

    def _build_ui(self):
        pad_x = (30, 10)

        style = ttk.Style(self.editScreen)
        style.configure("Grey.TLabel", background="grey74")

        ttk.Label(self.editScreen, text="Site / Service:", style="Grey.TLabel").grid(
            row=0, column=0, padx=pad_x, pady=(20, 5), sticky="e",
        )
        self.site_entry = ttk.Entry(self.editScreen, width=40)
        self.site_entry.grid(row=0, column=1, pady=(20, 5), sticky="w")

        ttk.Label(self.editScreen, text="Username / Email:", style="Grey.TLabel").grid(
            row=1, column=0, padx=pad_x, pady=(5, 5), sticky="e"
        )
        self.username_entry = ttk.Entry(self.editScreen, width=40)
        self.username_entry.grid(row=1, column=1, pady=(5, 5), sticky="w")

        ttk.Label(self.editScreen, text="Password:", style="Grey.TLabel").grid(
            row=2, column=0, padx=pad_x, pady=(5, 5), sticky="e"
        )
        self.password_entry = ttk.Entry(self.editScreen, width=40, show="*")
        self.password_entry.grid(row=2, column=1, pady=(5, 5), sticky="w")

        ttk.Label(self.editScreen, text="Notes (optional):", style="Grey.TLabel").grid(
            row=3, column=0, padx=pad_x, pady=(5, 5), sticky="ne"
        )
        self.notes_text = tk.Text(self.editScreen, width=30, height=4)
        self.notes_text.grid(row=3, column=1, pady=(5, 10), sticky="w")

        button_text = "Save"
        add_button = ttk.Button(self.editScreen, text=button_text, command=self.save_click)
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
        self.editScreen.destroy()
