import tkinter as tk
from loginScreen import LoginScreen
from vaultScreen import VaultScreen




class PasswordManager:
    def __init__(self):
        self.show_login()


    def show_login(self):
        self.root = tk.Tk()
        self.loginScreen = LoginScreen(self.root, self.show_vault)

    def show_vault(self):
        self.root = tk.Tk()
        self.vaultScreen = VaultScreen(self.root)


    def run(self):
        self.root.mainloop()




