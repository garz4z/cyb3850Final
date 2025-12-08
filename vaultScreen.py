import tkinter as tk
from tkinter import ttk
from addScreen import AddScreen
from loginScreen import LoginScreen



class VaultScreen:
    def __init__(self, root, signout):
        self.root = root
        self.signout = signout
        self.root.title("Password Manager")
        self.root.geometry("800x600")

        self.generate_elements()


    def generate_elements(self):

        vault_label = ttk.Label(self.root, text="User's Vault")
        vault_label.configure(font=("Arial", 14))

        signout_button = ttk.Button(
            self.root,
            text="Sign Out",
            command=self.signout_click
        )

        add_button = ttk.Button(
            self.root,
            text="Add New Password",
            command=self.add_password_click
        )


        vault_label.grid(column=0, row=0, pady=(5, 0), padx=10, sticky="w")
        add_button.grid(column=0, row=0, pady=(5, 0), padx=10, sticky="e")
        signout_button.grid(column=1, row=0, pady=(5, 0), padx=10, sticky="ne")



        self.generate_table()

    def generate_table(self):
        self.root.rowconfigure(1, weight=1)
        self.root.columnconfigure(0, weight=1)

        frame = ttk.Frame(self.root)
        frame.grid(column=0, row=1, columnspan=2, padx=10, pady=5, sticky="nsew")


        column_labels = ('Username', 'Password', 'Date Added')
        table = ttk.Treeview(frame, columns=column_labels, show="headings", height=10)
        table.heading("Username", text="Username")
        table.heading("Password", text="Password")
        table.heading("Date Added", text="Date Added")

        table.column("Username", stretch=tk.YES)
        table.column("Password", stretch=tk.YES)
        table.column("Date Added", width=80, stretch=tk.NO)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
        table.configure(yscrollcommand=scrollbar.set)

        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        table.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # This is where the data would be added
        for i in range(50):
            table.insert("", "end", values=("Example Username", "Example Password"))

    def signout_click(self):
        self.root.destroy()
        self.signout()


    def add_password_click(self):
        AddScreen(self.root)