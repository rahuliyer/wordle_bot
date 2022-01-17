#! /usr/bin/python

import random

def get_word_list():
    with open('/usr/share/dict/words') as f:
        lines = f.readlines()

        word_list = set()
        for word in lines:
            word = word.strip()
            word = word.lower()

            if len(word) == 5:
                word_list.add(word)

        return word_list

class WordleBot:
    def __init__(self, word_list):
        self.word_list = word_list

        self.letter2word = {}
        self.letterpos2word = {}

        self.reset_state()

    def reset_state(self):
        self.word_hash = {
            0: None,
            1: None,
            2: None,
            3: None,
            4: None
        }

        self.incorrect_pos_letters = {}
        self.not_in_word = set()
        self.in_word = set()

    def process_word_list(self):
        for word in self.word_list:
            for i in range(len(word)):
                letter = word[i]
                if letter not in self.letter2word:
                    self.letter2word[letter] = set()

                self.letter2word[letter].add(word)

                if letter not in self.letterpos2word:
                    self.letterpos2word[letter] = {}

                if i not in self.letterpos2word[letter]:
                    self.letterpos2word[letter][i] = set()

                self.letterpos2word[letter][i].add(word)

    def update_state(self, guess, result):
        if result == "":
            return

        for i in range(len(result)):
            if result[i] == 'G':
                self.word_hash[i] = guess[i]
                self.in_word.add(guess[i])
            elif result[i] == 'Y':
                if guess[i] not in self.incorrect_pos_letters:
                    self.incorrect_pos_letters[guess[i]] = set()

                self.incorrect_pos_letters[guess[i]].add(i)
                self.in_word.add(guess[i])
            else:
                if guess[i] not in self.in_word:
                    self.not_in_word.add(guess[i])

    def generate_candidate_set(self):
        candidate_set = self.word_list.copy()

        for pos in self.word_hash:
            if self.word_hash[pos] != None:
                candidate_set &= self.letterpos2word[self.word_hash[pos]][pos]

        for letter in self.incorrect_pos_letters:
            candidate_set &= self.letter2word[letter]

        for letter in self.incorrect_pos_letters:
            for pos in self.incorrect_pos_letters[letter]:
                candidate_set -= self.letterpos2word[letter][pos]

        for letter in self.not_in_word:
            candidate_set -= self.letter2word[letter]

        return candidate_set

    def check4win(self):
        for i in self.word_hash:
            if self.word_hash[i] == None:
                return False

        return True

    def evaluate_guess(self, word, guess):
        result = ""

        for i in range(len(guess)):
            if guess[i] not in word:
                result += 'B'
            elif guess[i] == word[i]:
                result += 'G'
            else:
                result += 'Y'

        return result

    def play(self, word, verbose=False):
        guess = "stone"
        turns = 1

        if verbose == True:
            print("Word: %s" % word)
            print("Guess: %s" % guess)

        while True:
            if word == None:
                result = raw_input("enter result: ")
                result = result.strip()
            else:
                result = self.evaluate_guess(word, guess)

            self.update_state(guess, result)

            if self.check4win():
                return turns

            candidate_set = self.generate_candidate_set()
            guess = random.sample(candidate_set, 1)[0]

            if verbose == True:
                print("Next guess: %s" % guess)

            turns += 1

    def interactive_play(self):
        return self.play(None, True)

    def test_preprocessing(self):
        word = "abbey"

        print("abbey in letter2word['a']: %s" % str(word in self.letter2word['a']))
        print("abbey in letter2word['b']: %s" % str(word in self.letter2word['b']))
        print("abbey in letter2word['x']: %s" % str(word in self.letter2word['x']))
        print("abbey in letterpos2word['b'][1]: %s" % str(word in self.letterpos2word['b'][1]))
        print("abbey in letterpos2word['b'][2]: %s" % str(word in self.letterpos2word['b'][2]))
        print("abbey in letterpos2word['b'][3]: %s" % str(word in self.letterpos2word['b'][3]))

def evaluate_solution(bot, word_list):
    plays = 5000
    words = random.sample(word_list, plays)

    sum = 0.0
    histogram = {}

    for i in range(plays):
        word = words[i]
        turns = bot.play(word, False)

        sum += turns
        if turns not in histogram:
            histogram[turns] = 1
        else:
            histogram[turns] += 1

        bot.reset_state()

    for key in histogram:
        print("%d turns: %d" % (key, histogram[key]))

    print("Average number of turns: %f" % (sum / plays))

if __name__ == "__main__":
    random.seed()
    word_list = get_word_list()

    bot = WordleBot(word_list)
    bot.process_word_list()

#    evaluate_solution(bot, word_list)

    print("Success! Guessed in %d turns" % bot.interactive_play())
