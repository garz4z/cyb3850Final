import tkinter as tk
from tkinter import ttk

from addScreen import AddScreen


class VaultScreen:
    def __init__(self, root, app):
        """
        root: main Tk root
        app: PasswordManager instance (holds current_user_id, current_key, db, crypto)
        """
        self.root = root
        self.app = app

        self.root.title("Password Manager - Vault")

        # Holds decrypted entries from DB so we can search/filter without re-querying
        self.all_entries = []

        self._build_ui()
        self.refresh_entries()  # load from DB + render

    def _build_ui(self):
        # Header row
        header = ttk.Frame(self.root)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=5, padx=10)

        title = ttk.Label(
            header,
            text=f"{self.app.current_username}'s Vault" if self.app.current_username else "Vault",
        )
        title.configure(font=("Arial", 14, "bold"))
        title.grid(row=0, column=0, padx=(0, 15), sticky="w")

        # --- Search UI (FR5) ---
        ttk.Label(header, text="Search:").grid(row=0, column=1, sticky="e")
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(header, textvariable=self.search_var, width=28)
        search_entry.grid(row=0, column=2, padx=(5, 10), sticky="w")

        search_btn = ttk.Button(header, text="Search", command=self.apply_search)
        search_btn.grid(row=0, column=3, padx=(0, 10), sticky="w")

        clear_btn = ttk.Button(header, text="Clear", command=self.clear_search)
        clear_btn.grid(row=0, column=4, padx=(0, 15), sticky="w")

        # Optional: live filter as you type
        search_entry.bind("<KeyRelease>", lambda e: self.apply_search())

        # --- Buttons ---
        add_btn = ttk.Button(header, text="Add New Password", command=self.add_password_click)
        add_btn.grid(row=0, column=5, padx=(0, 10), sticky="e")

        signout_btn = ttk.Button(header, text="Sign Out", command=self.signout_click)
        signout_btn.grid(row=0, column=6, sticky="e")

        # Make header spacing behave nicely
        header.columnconfigure(0, weight=1)

        # Table area
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        frame = ttk.Frame(self.root)
        frame.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        columns = ("Site", "Username", "Password", "Date Added")
        self.table = ttk.Treeview(frame, columns=columns, show="headings", height=15)

        for col in columns:
            self.table.heading(col, text=col)

        self.table.column("Site", width=220, stretch=tk.YES)
        self.table.column("Username", width=220, stretch=tk.YES)
        self.table.column("Password", width=220, stretch=tk.YES)
        self.table.column("Date Added", width=140, stretch=tk.NO)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=scrollbar.set)

        self.table.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

    # ---------------- Data loading + rendering ----------------

    def refresh_entries(self):
        """Pull decrypted entries from DB for the logged-in user and display them."""
        if self.app.current_user_id is None or self.app.current_key is None:
            self.all_entries = []
            self.render_entries([])
            return

        self.all_entries = self.app.db.get_entries_for_user(
            self.app.current_user_id,
            self.app.current_key,
            self.app.crypto
        )

        # Apply current search term to refreshed data
        self.apply_search()

    def render_entries(self, entries):
        """Clear the table and insert entries."""
        for item in self.table.get_children():
            self.table.delete(item)

        for e in entries:
            self.table.insert(
                "",
                "end",
                values=(
                    e.get("site", ""),
                    e.get("username", ""),
                    e.get("password", ""),
                    e.get("created_at", ""),
                ),
            )

    # ---------------- Search (FR5) ----------------

    def apply_search(self):
        """Filter by site OR username (case-insensitive)."""
        q = self.search_var.get().strip().lower()
        if not q:
            self.render_entries(self.all_entries)
            return

        filtered = []
        for e in self.all_entries:
            site = (e.get("site") or "").lower()
            username = (e.get("username") or "").lower()
            if q in site or q in username:
                filtered.append(e)

        self.render_entries(filtered)

    def clear_search(self):
        self.search_var.set("")
        self.render_entries(self.all_entries)

    # ---------------- Buttons ----------------

    def signout_click(self):
        self.app.sign_out()

    def add_password_click(self):
        # Open AddScreen and refresh after save
        AddScreen(self.root, app=self.app, on_saved=self.refresh_entries)
