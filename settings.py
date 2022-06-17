import tkinter as tk
import sqlite3
from tkinter import messagebox


class Settings:
    def __init__(self, functions):
        self.functions = functions
        self.root = functions.root
        self.window = tk.Toplevel(self.root)

        self.window.protocol("WM_DELETE_WINDOW", self.close)

        self.root.attributes('-disabled', True)

        self.window.geometry("400x300+300+120")
        self.window.config(background="grey")

        self.high_score_value = tk.IntVar()
        self.high_score = tk.Entry(self.window,textvariable=self.high_score_value)
        self.high_score.pack(pady=5)

        self.length = tk.IntVar()
        self.word_length = tk.Entry(self.window,textvariable=self.length)
        self.word_length.pack()
        self.get_current_db()

        self.change_word_length = tk.Button(self.window,text="Change",command=self.change_db,font="lucida 12 bold",bg="black",fg="sky blue")
        self.change_word_length.pack(pady=5)

    def get_current_db(self):
        connection = sqlite3.connect("settings.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM info")
        data = cursor.fetchall()
        self.length.set(data[0][1])
        self.high_score_value.set(data[0][2])

        connection.close()

    def change_db(self):

        if not self.high_score.get() or not self.word_length.get():
            messagebox.showinfo("Error !!!", f"Word Length and High Score can't be empty.")
            self.window.focus_force()
            return

        if self.word_length.get():
            if self.length.get() > 5 or self.length.get() < 3:
                messagebox.showinfo("Error !!!", f"Word Length can't be less than 3 or greater than 5")
                self.window.focus_force()
                return

        connection = sqlite3.connect("settings.db")
        cursor = connection.cursor()

        cursor.execute(f"UPDATE info SET word_length={self.length.get()} WHERE id=0")
        cursor.execute(f"UPDATE info SET high_score={self.high_score_value.get()} WHERE id=0")

        connection.commit()
        connection.close()

        self.functions.get_from_db()
        self.functions.show_buttons()

        self.root.attributes('-disabled', False)

        self.root.focus_force()
        self.window.destroy()

    def close(self):
        self.window.destroy()
        self.root.focus_force()
        self.root.attributes('-disabled', False)

