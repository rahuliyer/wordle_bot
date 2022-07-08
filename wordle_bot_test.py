import unittest
from main import *

class TestWordleBot(unittest.TestCase):
  def setUp(self):
    self.bot = WordleBot()
    self.bot.word_list = set([
      'marry',
      'batty',
      'floss',
      'fresh',
      'crust',
      'stool',
      'colon',
      'pride',
      'croak',
      'major',
      'react',
      'paddy',
      'daddy'
    ])

    self.letter2word = {
      'a': set([
        'marry',
        'batty',
        'croak',
        'major',
        'react',
        'paddy',
        'daddy'
      ]),
      'b': set([
        'batty',
      ]), 
      'c': set([
        'crust',
        'colon',
        'croak',
        'react'
      ])
    }

    self.letterpos2word = {
      'r': {
        0: set([
          'react'
        ]),
        1: set([
          'fresh',
          'crust',
          'pride',
          'croak'
        ]),
        2: set([
          'marry'
        ]),
        3: set([
          'marry'
        ]),
        4: set([
          'major'
        ])
      },
      'm': {
        0: set([
          'marry',
          'major'
        ])
      }
    }

    self.letterfreq2word = {
      'r': {
        1: set([
          'fresh',
          'crust',
          'pride',
          'react',
          'croak',
          'major'
        ]),
        2: set([
          'marry'
        ]),
      },
      'd': {
        1: set([
          'pride'
        ]),
        2: set([
          'paddy'
        ]),
        3: set([
          'daddy'
        ])
      }
    }
    
    self.bot.process_word_list()

  def testLetter2Word(self):
    self.assertEqual(
      self.letter2word['a'], 
      self.bot.letter2word['a']
    )

    self.assertEqual(
      self.letter2word['b'], 
      self.bot.letter2word['b']
    )

    self.assertEqual(
      self.letter2word['c'], 
      self.bot.letter2word['c']
    )

  def testLetterPos2Word(self):
    self.assertEqual(
      self.letterpos2word['r'],
      self.bot.letterpos2word['r']
    )

    self.assertEqual(
      self.letterpos2word['m'],
      self.bot.letterpos2word['m']
    )

  def testLetterFreq2Word(self):
    self.assertEqual(
      self.letterfreq2word['r'],
      self.bot.letterfreq2word['r']      
    )

    self.assertEqual(
      self.letterfreq2word['d'],
      self.bot.letterfreq2word['d']      
    )
  
  def testLetterFreq(self):
    letter_freq = self.bot.generate_letter_freq("MADDY")
    self.assertEqual(
      letter_freq,
      {
        'M': 1,
        'A': 1,
        'D': 2,
        'Y': 1
      }
    )

  def testSolutionEval(self):
    self.assertEqual(
      self.bot.evaluate_guess("AGAPE", "SOARE"),
      "BBGBG"
    )

    self.assertEqual(
      self.bot.evaluate_guess("DAWDY", "DADDY"),
      "GGYBG"
    )

    self.assertEqual(
      self.bot.evaluate_guess("ABYSS", "ABBAS"),
      "GGBBG"
    )

  def testHandleGreen(self):
    res = self.bot.handle_green('r', 1)

    self.assertEqual(set([
      'fresh',
      'crust',
      'pride',
      'croak'
    ]), res)

  def testHandleYellow(self):
    res = self.bot.handle_yellow('r', 1)

    self.assertEqual(set([
      'marry',
      'major',
      'react'
    ]), res)

  def testHandleBlackLetterDoesntExist(self):
    res = self.bot.handle_black('r', {
      'a': 1,
      'b': 2
    })

    self.assertEqual(set([
      'batty',
      'floss',
      'stool',
      'colon',
      'paddy',
      'daddy'
    ]), res)

  def testHandleBlackLetterExists(self):
    res = self.bot.handle_black('d', {
      'd': 2,
    })

    self.assertEqual(set(['paddy']), res)

  def testCandidateSetExcludesGuess(self):
    guess = "floss"
    self.bot.update_candidate_set(guess, "GBBGB")

    self.assertFalse(guess in self.bot.candidate_set)