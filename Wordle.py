import tkinter as tk
from PIL import Image, ImageTk
import ctypes
import words_api
import settings as st
import os
import sqlite3

ctypes.windll.shcore.SetProcessDpiAwareness(1)


class Wordle:
    FIRST_RIGHT = 10
    BG = "#171717"
    MAX_SCORE = 12

    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("600x800+400+150")

        # bg="white"
        self.root.configure(background=self.BG)

        self.guess = ""
        self.won = False
        self.guess_count = 0
        self.score = 0
        self.word_size = 5
        self.high_score = 0
        self.word_api = None
        self.get_from_db()

        self.setting = Image.open('images/setting.png')
        self.setting = self.setting.resize((40, 40), Image.Resampling.LANCZOS)
        self.setting = ImageTk.PhotoImage(self.setting)

        self.setting_dark = Image.open('images/setting_dark.png')
        self.setting_dark = self.setting_dark.resize((40, 40), Image.Resampling.LANCZOS)
        self.setting_dark = ImageTk.PhotoImage(self.setting_dark)

        label = Image.open('images/head.png')
        # label = label.resize((402, 100), Image.Resampling.LANCZOS)
        label = ImageTk.PhotoImage(label)

        top_frame = tk.Frame(self.root, bg=self.BG)
        top_frame.pack(fill="x")

        sett = tk.Button(top_frame, image=self.setting,command=self.open_setting, bd=0, bg=self.BG, cursor="hand2", activebackground=self.BG)
        sett.pack(side="right")
        sett.bind("<Enter>", self.on_hover)
        sett.bind("<Leave>", self.off_hover)

        head = tk.Label(self.root, image=label, bd=0, bg=self.BG)
        head.pack()

        # word buttons

        main_btn_frame = tk.Frame(self.root, bg=self.BG)
        main_btn_frame.pack(pady=15)

        f1 = tk.Frame(main_btn_frame, bg=self.BG)
        f2 = tk.Frame(main_btn_frame, bg=self.BG)
        f3 = tk.Frame(main_btn_frame, bg=self.BG)
        f4 = tk.Frame(main_btn_frame, bg=self.BG)
        f5 = tk.Frame(main_btn_frame, bg=self.BG)
        f6 = tk.Frame(main_btn_frame, bg=self.BG)
        self.button_frames = [f1, f2, f3, f4, f5, f6]

        self.b_row1 = self.b_row2 = self.b_row3 = self.b_row4 = self.b_row5 = self.b_row6 = []
        self.buttons = []

        self.current_B_row = 0
        self.current_b = 0

        self.show_buttons()

        # keypad buttons

        keyboard_frame = tk.Frame(self.root, bg=self.BG)
        keyboard_frame.pack(pady=5)

        c = 65

        f1 = tk.Frame(keyboard_frame, bg=self.BG)
        f1.pack(side="top", pady=2)
        f2 = tk.Frame(keyboard_frame, bg=self.BG)
        f2.pack(side="top", pady=2)
        f3 = tk.Frame(keyboard_frame, bg=self.BG)
        f3.pack(side="top", pady=2)

        f = [f1, f2, f3]
        step = 6
        self.keypad_buttons = [[], [], []]

        self.keypad_btn_pos = {0: [chr(i) for i in range(65, 71)],
                               1: [chr(i) for i in range(71, 81)],
                               2: [chr(i) for i in range(81, 91)]}

        key_pad_color = "#ff7700"
        index = 0
        for i in range(3):
            for _ in range(step):
                b = tk.Button(f[index], text=chr(c), font="cambria 13 bold", bg=self.BG,
                              fg=key_pad_color, cursor="hand2", padx=3)
                b.pack(side="left", padx=2)
                self.keypad_buttons[i].append(b)
                b.bind("<Button-1>", lambda e: self.key_press(keyboard=e))
                b.bind("<Enter>", lambda e: on_hover(e, "#575656"))
                b.bind("<Leave>", lambda e: off_hover(e, self.BG))
                c += 1
            if i == 0:
                b = tk.Button(f[index], text="Enter", font="cambria 13 bold", bg=self.BG,
                              fg=key_pad_color, cursor="hand2")
                b.pack(side="left", padx=2)
                b.bind("<Button-1>", lambda e: self.key_press(keyboard=e))
                b.bind("<Enter>", lambda e: on_hover(e, "#575656"))
                b.bind("<Leave>", lambda e: off_hover(e, self.BG))
            if i == 0:
                b = tk.Button(f[index], text="←", font="cambria 13 bold", bg=self.BG,
                              fg=key_pad_color, cursor="hand2")
                b.pack(side="left", padx=2)
                b.bind("<Button-1>", lambda e: self.key_press(keyboard=e))
                b.bind("<Enter>", lambda e: on_hover(e, "#575656"))
                b.bind("<Leave>", lambda e: off_hover(e, self.BG))
            index += 1
            step = 10

        self.root.bind("<KeyRelease>", self.key_press)

        self.root.mainloop()

    def show_buttons(self):
        if self.buttons:
            for b in self.buttons:
                if b:
                    for i in b:
                        i.destroy()

        self.b_row1 = self.b_row2 = self.b_row3 = self.b_row4 = self.b_row5 = self.b_row6 = []
        self.buttons = []

        self.current_B_row = 0
        self.current_b = 0

        for i in range(6):
            row_btn = []
            self.button_frames[i].pack(pady=4)
            for j in range(self.word_size):
                b = tk.Button(self.button_frames[i], text="", fg="white", bd=2,
                              font="lucida 18", bg=self.BG, width=3, height=1)
                b.pack(side="left", padx=2)

                row_btn.append(b)
            self.buttons.append(row_btn)

    def key_press(self, e=None, keyboard=None):
        if e:
            if e.keysym == "BackSpace":
                self.erase_character()

            elif e.keysym == "Return":
                self.check_for_match()

            elif 65 <= e.keycode <= 90:
                key = e.char
                if self.current_b == self.word_size:
                    self.current_b = self.word_size - 1

                    characters = list(self.guess)
                    characters[self.current_b] = ""
                    self.guess = "".join(characters)

                self.buttons[self.current_B_row][self.current_b]["text"] = key.upper()
                self.guess += key.upper()
                self.current_b += 1
            else:
                print(e.keysym)
        else:
            key_press = keyboard.widget
            if key_press['text'] == 'Enter':
                self.check_for_match()
            elif key_press['text'] == '←':
                self.erase_character()
            else:
                if self.current_b == self.word_size:
                    self.current_b = self.word_size - 1

                    characters = list(self.guess)
                    characters[self.current_b] = ""
                    self.guess = "".join(characters)

                self.buttons[self.current_B_row][self.current_b]["text"] = key_press['text']
                self.guess += key_press['text']
                self.current_b += 1

    def erase_character(self):
        if self.current_b > 0:
            self.current_b -= 1
            self.guess = self.guess[0: self.current_b]
            self.buttons[self.current_B_row][self.current_b]["text"] = ""
            print("word = ", self.guess)

    def check_for_match(self):
        if len(self.guess) == self.word_size:
            self.guess_count += 1

            if self.word_api.is_valid_guess(self.guess):
                for button in self.buttons[self.current_B_row]:
                    button["bg"] = "green"

                # changing the keypad color
                self.change_keypad_color("#00ff2a", self.guess)

                self.won = True
                self.score += self.MAX_SCORE - 2 * (self.guess_count - 1)

                if self.score > self.high_score:
                    self.update_high_score()

                print("You won !!!")
                self.word_api.select_word()
                self.show_popup()
            else:
                if self.guess_count == 6:
                    print("You Lost !!!")
                    self.show_popup()
                    self.word_api.select_word()
                    return
                for i in range(self.word_size):
                    if self.word_api.is_at_right_position(i, self.guess[i]):
                        self.buttons[self.current_B_row][i]['bg'] = "green"

                        # changing the keypad color
                        self.change_keypad_color("#0fd630", self.guess[i], "#239436", "#0fd630")

                        """
                         if a character is present more than once in a word then we will only
                         change the color of, that comes first, That's why we are replacing the 
                         duplicates with '/' so that the duplicates are not highlighted.
                        """
                        characters = list(self.guess)
                        for index, char in enumerate(characters):
                            if self.word_api.is_at_right_position(i, char):
                                characters[index] = '/'

                        self.guess = "".join(characters)

                    elif self.word_api.is_in_word(self.guess[i]):
                        self.buttons[self.current_B_row][i]['bg'] = "#d0d925"

                        # changing the keypad color
                        self.change_keypad_color("#d0d925", self.guess[i], "#9ba128", "#d0d925")

                        """
                         if a character is present more than once in a word then we will only
                         change the color of, that comes first, That's why we are replacing the 
                         duplicates with '/' so that the duplicates are not highlighted.
                        """
                        characters = list(self.guess)
                        for index, char in enumerate(characters):
                            if char == self.guess[i] and index != i:
                                characters[index] = '/'
                            # if self.word_api.is_at_right_position(i, char):
                            #     characters[index] = '/'

                        self.guess = "".join(characters)

            self.current_b = 0
            self.current_B_row += 1
            self.guess = ""

    def reset(self, popup=None):
        for buttons_list in self.buttons:
            for button in buttons_list:
                button["text"] = ""
                button["bg"] = self.BG

        for buttons_list in self.keypad_buttons:
            for button in buttons_list:
                button["bg"] = self.BG
                button.bind("<Enter>", lambda e: on_hover(e, "#575656"))
                button.bind("<Leave>", lambda e: off_hover(e, self.BG))

        self.current_b = self.current_B_row = 0
        self.won = False
        self.guess_count = 0
        self.guess = ""

        self.root.attributes('-disabled', False)
        self.root.focus_get()
        if popup:
            popup.destroy()

    def show_popup(self):
        popup = tk.Toplevel()
        popup.geometry("450x250+500+160")
        popup.configure(background="black")
        popup.focus_set()

        status = "You Lost :("

        if self.won:
            status = "You Won !!!"

        status_label = tk.Label(popup, text=status, font="cambria 20 bold", fg="#14f41f", bg="black")
        status_label.pack(pady=10)

        if not self.won:
            right_word = tk.Label(popup, text=f"The word was {self.word_api.word}", font="cambria 15 bold",
                                  fg="#14f41f", bg="black")
            right_word.pack(pady=3)

        score_label = tk.Label(popup, text=f"Score : {self.score}", font="lucida 15 bold", fg="white", bg="black")
        score_label.pack(pady=4)

        high_score_label = tk.Label(popup, text=f"High Score : {self.high_score}", font="lucida 15 bold", fg="white", bg="black")
        high_score_label.pack(pady=4)

        button = tk.Button(popup, text="Okay", font="lucida 12 bold", fg="#00d0ff", cursor="hand2",
                           bg="#252525", padx=10, command=lambda: self.reset(popup))
        button.pack(pady=4)

        # disable the main window, will get enabled only when popup is closed
        self.root.attributes('-disabled', True)

        def close():
            self.reset(popup)

        popup.protocol("WM_DELETE_WINDOW", close)

    def change_keypad_color(self, color, guess, on_hover_color=None, off_hover_color=None):
        for char in guess:
            if 65 <= ord(char) <= 70:
                btn_frame_index = 0
                btn_index = ord(char) - 65
            elif 71 <= ord(char) <= 80:
                btn_frame_index = 1
                btn_index = ord(char) - 71
            else:
                btn_frame_index = 2
                btn_index = ord(char) - 81
            self.keypad_buttons[btn_frame_index][btn_index]['bg'] = color

            if on_hover_color:
                self.keypad_buttons[btn_frame_index][btn_index].bind("<Enter>", lambda e: on_hover(e, on_hover_color))
                self.keypad_buttons[btn_frame_index][btn_index].bind("<Leave>", lambda e: off_hover(e, off_hover_color))

    def get_from_db(self):
        if not os.path.exists("settings.db"):
            connection = sqlite3.connect("settings.db")
            cursor = connection.cursor()
            cursor.execute("CREATE TABLE info(id integer, word_length integer,high_score integer)")
            cursor.execute('INSERT INTO info VALUES(?,?,?)', (0, 5, 0))

            self.word_api = words_api.Words(self.word_size)

            connection.commit()
            cursor.execute("SELECT * FROM info")
            connection.close()
        else:
            connection = sqlite3.connect("settings.db")
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM info")

            data = cursor.fetchall()
            self.word_size = data[0][1]
            self.high_score = data[0][2]

            print("high = ",self.high_score)
            print("word size = ",self.word_size)

            self.word_api = words_api.Words(self.word_size)

            connection.close()

    def update_high_score(self):
        connection = sqlite3.connect("settings.db")
        cursor = connection.cursor()

        self.high_score = self.score
        print("update score = ",self.high_score)
        cursor.execute(f"UPDATE info SET high_score={self.score} WHERE id=0")
        connection.commit()

        connection.close()

    def open_setting(self):
        setting = st.Settings(self)

    def on_hover(self, e):
        widget = e.widget
        widget["image"] = self.setting_dark

    def off_hover(self, e):
        widget = e.widget
        widget["image"] = self.setting


def on_hover(e, color):
    button = e.widget
    button["bg"] = color


def off_hover(e, color):
    button = e.widget
    button["bg"] = color


if __name__ == '__main__':
    Wordle()
