import random


class Words:
    def __init__(self, size):
        self.size = size
        self.words_list = []
        self.used_words = []
        self.word = ""

        self.load_words()
        self.select_word()

    def load_words(self):
        if self.size == 3:
            file_name = 'three_letters'
        elif self.size == 4:
            file_name = 'four_letters'
        elif self.size == 5:
            file_name = 'five_letters'
        else:
            file_name = 'six_letters'

        with open(f"C://Users//hp//Desktop//{file_name}.txt", 'r') as file:
            self.words_list = file.readlines()

        self.words_list = [word.strip('\n') for word in self.words_list]

    def is_at_right_position(self, i, char):
        if self.word[i] == char:
            return True
        return False

    def is_in_word(self, char):
        if char in self.word:
            return True
        return False

    def is_valid_guess(self, guess):
        if guess == self.word:
            return True
        return False

    def select_word(self):
        self.word = random.choice(self.words_list).upper()
        while self.word in self.used_words:
            self.word = random.choice(self.words_list).upper()
        self.used_words.append(self.word)

    def display_right_word(self):
        print("Right word was : ",self.word)





