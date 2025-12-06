import tkinter as tk
from tkinter import ttk
from addScreen import AddScreen



class VaultScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Manager")
        self.root.geometry("800x600")

        self.generate_elements()


    def generate_elements(self):
        add_button = ttk.Button(
            self.root,
            text="New Password",
            command=self.add_password_click
        )

        add_button.grid(column=0, row=0)


    def add_password_click(self):
        AddScreen(self.root)