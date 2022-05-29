import tkinter as tk


class Settings:
    def __init__(self, root):
        self.root = root
        self.window = tk.Toplevel(self.root)

        self.window.geometry("400x300+300+120")
        self.window.config(background="grey")