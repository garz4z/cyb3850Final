import tkinter as tk
from tkinter import ttk



class LoginScreen:
    def __init__(self, root, login):
        self.root = root
        self.login = login
        self.root.title("Login Password Manager")
        self.root.geometry("400x300")

        self.generate_elements()


    def generate_elements(self):

        username_entry = ttk.Entry(self.root, width=40)
        password_entry = ttk.Entry(self.root, width=40)
        username_entry.focus()
        password_entry.focus()

        login_button = ttk.Button(
            self.root,
            text="Login",
            command=self.login_click
        )

        username_entry.grid(row=0, column=1, padx=80, pady=(100, 10))
        password_entry.grid(row=1, column=1, pady=10)

        login_button.grid(row=3, column=1)

    def login_click(self):
        self.root.destroy()
        self.login()
