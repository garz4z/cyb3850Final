import tkinter as tk
from tkinter import ttk



class LoginScreen:
    def __init__(self, root, login):
        self.root = root
        self.login = login
        self.root.title("Login Password Manager")
        self.root.geometry("500x300")
        self.root.resizable(False, False)

        self.generate_elements()


    def generate_elements(self):

        username_entry = ttk.Entry(self.root, width=40)
        username_label = ttk.Label(self.root, text="Username: ")
        password_entry = ttk.Entry(self.root, width=40)
        password_label = ttk.Label(self.root, text="Password: ")
        username_entry.focus()
        password_entry.focus()

        login_button = ttk.Button(
            self.root,
            text="Login",
            command=self.login_click
        )

        user_button = ttk.Button(
            self.root,
            text="Create User",
            command=self.user_click
        )

        # pady=(100, 10)
        username_label.grid(row=0, column=0, padx=(60, 10), pady=(100, 5))
        username_entry.grid(row=0, column=1, pady=(100, 5))
        password_entry.grid(row=1, column=1, pady=(5, 5))
        password_label.grid(row=1, column=0, padx=(60, 10))

        login_button.grid(row=3, column=1, pady=5)
        user_button.grid(row=4, column=1)


    def login_click(self):
        self.root.destroy()
        self.login()

    def user_click(self):
        self.root.destroy()
