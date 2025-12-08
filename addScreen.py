import tkinter as tk
import tkinter.ttk as ttk

class AddScreen:
    def __init__(self, root):
        self.addScreen = tk.Toplevel(root)
        self.addScreen.title("Add Password")
        self.addScreen.resizable(False, False)
        self.addScreen.geometry("400x300")

        self.generate_elements()

    def generate_elements(self):
        username_entry = ttk.Entry(self.addScreen, width=40)
        username_label = ttk.Label(self.addScreen, text="Username: ")
        password_entry = ttk.Entry(self.addScreen, width=40)
        password_label = ttk.Label(self.addScreen, text="Password: ")
        username_entry.focus()
        password_entry.focus()

        username_label.grid(row=0, column=0, padx=(30, 10), pady=(100, 5))
        username_entry.grid(row=0, column=1, pady=(100, 5))
        password_entry.grid(row=1, column=1, pady=(5, 5))
        password_label.grid(row=1, column=0, padx=(30, 10))


        add_button = ttk.Button(
            self.addScreen,
            text="Add",
            command=self.add_click
        )
        add_button.grid(column=1, row=2)

    def add_click(self):
        self.addScreen.destroy()