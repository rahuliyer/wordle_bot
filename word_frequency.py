#!/usr/bin/python

from copyreg import pickle


import pickle

def get_word_frequencies():
#    with open('./full_word_list.txt') as f:
    with open('./wordle_2315.txt') as f:
        lines = f.readlines()

        word_list = set()
        for word in lines:
            word = word.strip()
            word = word.lower()

            if len(word) == 5 and word.isalpha():
                word_list.add(word)

    print("Number of words in the word list: %d" % len(word_list))

    with open('./unigram_freq.csv') as f:
        lines = f.readlines()

        word_frequencies = {}

        for line in lines:
            line = line.strip()
            word, freq = line.split(',')

            word = word.lower()
            freq = int(freq)

            if word in word_list:
                word_frequencies[word] = freq

    print("Number of words in the word frequency hash: %d" % len(word_frequencies))

    print("Fixing frequency list...")

    for word in word_list:
        if word not in word_frequencies:
            word_frequencies[word] = 1

    return word_list, word_frequencies

if __name__ == "__main__":
    word_list, word_frequencies = get_word_frequencies()

    pickle.dump(word_list, open("word_list.pkl", "wb"))
    pickle.dump(word_frequencies, open("word_frequencies.pkl", "wb"))

