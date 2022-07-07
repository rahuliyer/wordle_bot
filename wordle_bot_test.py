import unittest
from main import *

class TestWordleBot(unittest.TestCase):
  def setUp(self):
    self.bot = WordleBot()
    
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

  