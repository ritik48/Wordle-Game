import tkinter as tk
from PIL import Image,ImageTk
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)


class Wordle:
    FIRST_RIGHT = 10

    def __init__(self):
        self.root=tk.Tk()
        self.root.geometry("600x800+400+150")
        bg = "#171717"
        # bg="white"
        self.root.configure(background=bg)

        self.word = "NEONS"
        self.guess = ""
        self.won = False



        self.guess_count = 0




        img = Image.open('images\HEAD.png')
        # img=img.resize((200,100),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img)

        head = tk.Label(self.root, image=img, bd=0, bg=bg)
        head.pack()

        f = tk.Frame(self.root, bg=bg)
        f.pack(pady=15)
        self.root.bind("<KeyRelease>", self.key_press)

        self.b_row1 = self.b_row2 = self.b_row3 = self.b_row4 = self.b_row5 = self.b_row6 = []
        self.buttons = []

        f1 = tk.Frame(f, bg=bg)
        f2 = tk.Frame(f, bg=bg)
        f3 = tk.Frame(f, bg=bg)
        f4 = tk.Frame(f, bg=bg)
        f5 = tk.Frame(f, bg=bg)
        f6 = tk.Frame(f, bg=bg)
        self.button_frames = [f1,f2,f3,f4,f5,f6]

        self.current_B_row = 0
        self.current_b = 0

        for i in range(6):
            row_btn = []
            self.button_frames[i].pack(pady=4)
            for j in range(5):

                container = tk.Frame(self.button_frames[i], highlightbackground = "#b0b0b0",highlightthickness = 1, bd=0)
                container.pack(side="left",padx=4)

                b = tk.Button(container,text="",relief="flat", fg="white",bd=2, font="lucida 18", bg=bg, width=3, height=1)
                b.pack()

                row_btn.append(b)

            self.buttons.append(row_btn)

        self.root.mainloop()

    def key_press(self, e):
        if e.keysym == "BackSpace":
            self.erase_character()

        elif e.keysym == "Return":
            self.check_for_match()

        elif 65 <= e.keycode <= 90:
            key = e.char
            if self.current_b == 5:
                self.current_b = 4

                characters = list(self.guess)
                characters[self.current_b]=""
                self.guess = "".join(characters)

            self.buttons[self.current_B_row][self.current_b]["text"] = key.upper()
            self.guess += key.upper()
            self.current_b += 1
        else:
            print(e.keysym)

    def erase_character(self):
        if self.current_b > 0:
            self.current_b -= 1
            self.guess = self.guess[0: self.current_b]
            self.buttons[self.current_B_row][self.current_b]["text"] = ""
            print("word = ",self.guess)

    def check_for_match(self):
        if len(self.guess) == 5:
            self.guess_count += 1

            if self.guess == self.word:
                for button in self.buttons[self.current_B_row]:
                    button["bg"] = "green"
                self.won = True
                print("You won !!!")
                self.reset()
            else:
                if self.guess_count == 6:
                    print("You Lost !!!")
                    return
                for i in range(5):
                    if self.word[i] == self.guess[i]:
                        self.buttons[self.current_B_row][i]['bg']="green"

                        characters = list(self.guess)

                        for index, char in enumerate(characters):
                            if char == self.word[i]:
                                characters[index] = '/'

                        self.guess = "".join(characters)
                        print(self.guess)

                    elif self.guess[i] in self.word:
                        self.buttons[self.current_B_row][i]['bg'] = "yellow"

                        characters = list(self.guess)

                        for index, char in enumerate(characters):
                            if char == self.guess[i]:
                                characters[index] = '/'

                        self.guess = "".join(characters)
                        print(self.guess)

            self.current_b = 0
            self.current_B_row += 1
            self.guess = ""

    def reset(self):
        self.show_popup()

    def show_popup(self):
        popup = tk.Toplevel()
        popup.geometry("200x200+500+160")
        popup.configure(background="grey")





if __name__ == '__main__':
    Wordle()
