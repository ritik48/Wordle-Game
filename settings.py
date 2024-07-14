import tkinter as tk
from PIL import Image, ImageTk
import sqlite3
from tkinter import messagebox


class Settings:
    BG = "#171717"

    def __init__(self, functions):
        self.functions = functions
        self.root = functions.root

        self.window = tk.Toplevel(self.root)
        self.window.title("Settings")
        self.window.wm_iconbitmap('images/icon.ico')
        self.window.focus_force()

        self.window.protocol("WM_DELETE_WINDOW", self.close)

        self.root.attributes('-disabled', True)

        x_co = int(self.functions.width / 2 - (400 / 2)) + self.functions.x_co
        y_co = self.functions.y_co + int(self.functions.height / 2 - (200 / 2))

        self.window.geometry(f"400x200+{x_co}+{y_co}")
        self.window.config(background=self.BG)

        increase = Image.open("images/increase.png")
        increase = increase.resize((40, 40), Image.Resampling.LANCZOS)
        increase = ImageTk.PhotoImage(increase)

        decrease = Image.open("images/decrease.png")
        decrease = decrease.resize((40, 40), Image.Resampling.LANCZOS)
        decrease = ImageTk.PhotoImage(decrease)

        self.length = self.high_score_value = None

        length_frame = tk.Frame(self.window, background=self.BG)
        length_frame.pack(pady=10)

        tk.Label(length_frame, text="Size", background=self.BG, font="cambria 15 bold", fg="#14f41f").grid(row=0,column=0, padx=12)

        decrease_len_btn = tk.Button(length_frame, image=decrease, command=lambda: self.change_value(value="length",change="decrease")
                                     ,background=self.BG,border=0,cursor="hand2")
        decrease_len_btn.image = decrease
        decrease_len_btn.grid(row=0, column=1)
        decrease_len_btn.bind("<Enter>", self.on_hover)
        decrease_len_btn.bind("<Leave>", self.off_hover)

        self.word_length = tk.Label(length_frame, background=self.BG, font="cambria 15 bold", fg="white")
        self.word_length.grid(row=0,column=2,padx=15)

        increase_len_btn = tk.Button(length_frame, image=increase, command=lambda: self.change_value(value="length",change="increase")
                                     ,background=self.BG,border=0,cursor="hand2")
        increase_len_btn.image = increase
        increase_len_btn.grid(row=0, column=3)
        increase_len_btn.bind("<Enter>", self.on_hover)
        increase_len_btn.bind("<Leave>", self.off_hover)

        score_frame = tk.Frame(self.window, background=self.BG)
        score_frame.pack()

        tk.Label(score_frame, text="Score", background=self.BG, font="cambria 15 bold", fg="#14f41f").grid(row=0,column=0,padx=10)

        decrease_score_btn = tk.Button(score_frame, image=decrease, command=lambda: self.change_value(value="score",change="decrease")
                                       ,background=self.BG,border=0,cursor="hand2")
        decrease_score_btn.image = decrease
        decrease_score_btn.grid(row=0, column=1)
        decrease_score_btn.bind("<Enter>", self.on_hover)
        decrease_score_btn.bind("<Leave>", self.off_hover)

        self.high_score = tk.Label(score_frame, background=self.BG, font="cambria 15 bold", fg="white")
        self.high_score.grid(row=0,column=2,padx=15)

        increase_score_btn = tk.Button(score_frame, image=increase, command=lambda: self.change_value(value="score",change="increase")
                                       ,background=self.BG,border=0,cursor="hand2")
        increase_score_btn.image = increase
        increase_score_btn.grid(row=0, column=3)
        increase_score_btn.bind("<Enter>", self.on_hover)
        increase_score_btn.bind("<Leave>", self.off_hover)

        self.get_current_db()

        self.change_word_length = tk.Button(self.window,text="Change",command=self.change_db,font="lucida 12 bold",bg="black",fg="sky blue",cursor="hand2")
        self.change_word_length.pack(pady=15)
        self.change_word_length.bind("<Enter>", self.on_hover)
        self.change_word_length.bind("<Leave>", self.off_hover)

    def get_current_db(self):
        connection = sqlite3.connect("settings.db")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM info")
        data = cursor.fetchall()

        self.word_length["text"] = self.length = data[0][1]
        self.high_score["text"] = self.high_score_value = data[0][2]

        # self.length.set(data[0][1])
        # self.high_score_value.set(data[0][2])

        connection.close()

    def change_db(self):
        connection = sqlite3.connect("settings.db")
        cursor = connection.cursor()

        cursor.execute(f"UPDATE info SET word_length={self.length} WHERE id=0")
        cursor.execute(f"UPDATE info SET high_score={self.high_score_value} WHERE id=0")

        connection.commit()
        connection.close()

        self.functions.get_from_db()
        self.functions.show_buttons()
        self.functions.reset(keypad=True)


        self.root.attributes('-disabled', False)

        self.root.focus_force()
        self.window.destroy()

    def change_value(self, value=None, change=None):
        if value == "length":
            if change == "decrease":
                if 3 < self.length <= 6:
                    self.length -= 1

            elif change == "increase":
                if 3 <= self.length < 6:
                    self.length += 1

            self.word_length["text"] = self.length

        if value == "score":
            if change == "increase":
                self.high_score_value += 1

            elif change == "decrease":
                if self.high_score_value != 0:
                    self.high_score_value -= 1

            self.high_score["text"] = self.high_score_value

    def close(self):
        self.window.destroy()
        self.root.focus_force()
        self.root.attributes('-disabled', False)

    def on_hover(self, e):
        widget = e.widget
        widget["background"] = "#383838"

    def off_hover(self, e):
        widget = e.widget
        widget["background"] = self.BG

