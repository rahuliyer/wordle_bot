#! /usr/bin/python

import random
import pickle
import math
import os

class WordleBot:
    def get_word_list(self):
      with open("./word_list.pkl", "rb") as f:
        return pickle.load(f)
  
    def __init__(self):
      self.word_list = self.get_word_list()
      self.letter2word = {}
      self.letterpos2word = {}
      self.letterfreq2word = {}
      self.word_scores = {}

      with open("./word_frequencies.pkl", "rb") as f:
        self.word_frequencies = pickle.load(f)
        
      self.reset_state()
          
    def reset_state(self):
        self.candidate_set = self.word_list.copy()

    def process_letter2word(self, letter, word):
      if letter not in self.letter2word:
        self.letter2word[letter] = set()

      self.letter2word[letter].add(word)

    def process_letterpos2word(self, letter, word, pos):
      if letter not in self.letterpos2word:
          self.letterpos2word[letter] = {}

      if pos not in self.letterpos2word[letter]:
          self.letterpos2word[letter][pos] = set()

      self.letterpos2word[letter][pos].add(word)

    def process_letterfreq2word(self, word):
      letter_freq = self.generate_letter_freq(word)

      for letter in letter_freq:
        freq = letter_freq[letter]
        if letter not in self.letterfreq2word:
          self.letterfreq2word[letter] = {}

        if freq not in self.letterfreq2word[letter]:
          self.letterfreq2word[letter][freq] = set()

        self.letterfreq2word[letter][freq].add(word)

    def process_word_scores(self):
      if os.path.exists('./word_scores.pkl'):
        print("Found word_scores.pkl...")
        with open('./word_scores.pkl', "rb") as f:
          self.word_scores = pickle.load(f)
      else:
        print("word_scores.pkl not found. Calculating scores...")        
        self.word_scores = self.score_words()
        with open('./word_scores.pkl', "wb") as f:
          print("Writing word_scores.pkl...")
          pickle.dump(self.word_scores, f)

  
    def process_word_list(self):
        for word in self.word_list:
            for i in range(len(word)):
                letter = word[i]
                self.process_letter2word(letter, word)              
                self.process_letterpos2word(letter, word, i)

            self.process_letterfreq2word(word)

        self.process_word_scores()
  
    def handle_green(self, letter, pos):
      candidate_set = self.word_list.copy()

      candidate_set &= self.letterpos2word[letter][pos]

      return candidate_set

    def handle_yellow(self, letter, pos):
      candidate_set = set()

      for i in range(0, 5):
        if i != pos:
          candidate_set |= self.letterpos2word[letter][i]

      return candidate_set

    def handle_black(self, letter, processing_state):
      candidate_set = self.word_list.copy()

      if letter not in processing_state:
        candidate_set -= self.letter2word[letter]
      else:
        freq = processing_state[letter]
        candidate_set &= self.letterfreq2word[letter][freq]

      return candidate_set

    def get_processing_state(self, guess, result):
      processing_state = {}

      for i in range(0, len(guess)):
        if result[i] == 'G' or result[i] == 'Y':
          if guess[i] not in processing_state:
            processing_state[guess[i]] = 1
          else:
            processing_state[guess[i]] += 1

      return processing_state

    def calculate_new_candidate_set(self, guess, result):
      candidate_set = self.word_list.copy()

      for i in range(0, len(guess)):
        if result[i] == 'G':
          candidate_set &= self.handle_green(guess[i], i)
        elif result[i] == 'Y':
          candidate_set &= self.handle_yellow(guess[i], i)
        else:
          candidate_set &= self.handle_black(
            guess[i],
            self.get_processing_state(guess, result)
          )

      candidate_set.discard(guess)

      return candidate_set

    def update_candidate_set(self, guess, result):
      self.candidate_set &= self.calculate_new_candidate_set(guess, result)
      
      assert len(self.candidate_set) != 0

    def generate_letter_freq(self, word):
      letter_freq = {}

      for i in range(len(word)):
        if word[i] in letter_freq:
          letter_freq[word[i]] += 1
        else:
          letter_freq[word[i]] = 1

      return letter_freq
      
    def evaluate_guess(self, word, guess):
        result = ""
        letter_freq = self.generate_letter_freq(word)
      
        for i in range(len(guess)):
            if guess[i] not in word or letter_freq[guess[i]] == 0:
                result += 'B'
            elif guess[i] == word[i]:
                result += 'G'
                letter_freq[guess[i]] -= 1
            else:
                result += 'Y'
                letter_freq[guess[i]] -= 1

        return result

    def score_words(self):
      word_scores = {}
      for guess in self.candidate_set:
        cset_reduction = 0.0
        for target in self.candidate_set:
          result = self.evaluate_guess(target, guess)
          candidate_set = self.calculate_new_candidate_set(guess, result)
          cset_reduction += float(len(candidate_set)) / len(self.candidate_set)

        cset_reduction /= len(self.candidate_set)
        word_scores[guess] = math.log(cset_reduction) + math.log(self.word_frequencies[guess])

        print("Score for %s: %f" % (guess, word_scores[guess]))

      return word_scores

    def pick_best_word(self):
        best_score = -1
        best_word = None
      
        for word in self.candidate_set:          
            if self.word_scores[word] > best_score:
                best_score = self.word_scores[word]
                best_word = word

        return best_word

    def play(self, word, verbose=False):
        guess = self.pick_best_word() #"soare"
        turns = 1

        if verbose == True:
            print("Word: %s" % word)
            print("Guess: %s" % guess)

        while True:
            if word == None:
                result = input("enter result: ")
                result = result.upper().strip()
            else:
                result = self.evaluate_guess(word, guess)

            if result == "GGGGG":
              return turns

            self.update_candidate_set(guess, result)

            guess = self.pick_best_word()

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

def evaluate_solution(bot, word_list, print_failed_words=True, verbose=False):
    sum = 0.0
    histogram = {}
    failed_words = set()

    for word in word_list:
        bot.reset_state()
        turns = bot.play(word, verbose)

        if turns > 6:
            failed_words.add(word)

        sum += turns
        if turns not in histogram:
            histogram[turns] = 1
        else:
            histogram[turns] += 1

    for key in histogram:
        print("%d turns: %d" % (key, histogram[key]))

    print("Average number of turns: %f" % (sum / len(word_list)))

    if print_failed_words:
        print("Failed words: ")
        for word in failed_words:
            bot.reset_state()
            turns = bot.play(word, True)
            print("Number of turns: %d" % turns)

def get_wordle_list():
    wordles = set()
    with open("./wordles.txt") as f:
        lines = f.readlines()

        for word in lines:
            word = word.strip()
            word = word.lower()

            wordles.add(word)

    return wordles

if __name__ == "__main__":
    random.seed()

    bot = WordleBot()
    bot.process_word_list()

#    bot.play("abyss", True)
#    evaluate_solution(bot, get_wordle_list())
    bot.interactive_play()
#    print(bot.generate_letter_freq("MADDY"))  