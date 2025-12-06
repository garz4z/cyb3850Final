import tkinter as tk
import tkinter.ttk as ttk

class AddScreen:
    def __init__(self, root):
        self.addScreen = tk.Toplevel(root)
        self.addScreen.title("Add Password")
        self.addScreen.resizable(False, False)
        self.addScreen.geometry("400x400")

        self.generate_elements()

    def generate_elements(self):
        add_button = ttk.Button(
            self.addScreen,
            text="Add",
            command=self.add_click
        )
        add_button.grid(column=0, row=0)

    def add_click(self):
        self.addScreen.destroy()