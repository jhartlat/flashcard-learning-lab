import tempfile
import unittest
from pathlib import Path
from student.flashcards import parse_card, load_cards, check_answer, study_cards

class FlashcardTests(unittest.TestCase):
    def test_parse_valid(self):
        self.assertEqual(parse_card('  CPU? | Processor  \n'), {'front':'CPU?', 'back':'Processor'})
    def test_parse_missing_delimiter(self):
        self.assertIsNone(parse_card('CPU?'))
    def test_parse_extra_delimiter(self):
        self.assertIsNone(parse_card('CPU?|Processor|Other'))
    def test_parse_empty_side(self):
        self.assertIsNone(parse_card('CPU?|  '))
    def test_load_skips_invalid_and_preserves_order(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'cards.txt'
            path.write_text('A|1\ninvalid\nB|2\n|missing\n', encoding='utf-8')
            self.assertEqual(load_cards(str(path)), [{'front':'A','back':'1'}, {'front':'B','back':'2'}])
    def test_load_empty_file(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'empty.txt'
            path.write_text('', encoding='utf-8')
            self.assertEqual(load_cards(str(path)), [])
    def test_check_answer_normalizes(self):
        self.assertTrue(check_answer('  PARIS ', 'paris'))
        self.assertFalse(check_answer('London', 'Paris'))
    def test_study_score_and_feedback(self):
        cards = [{'front':'A','back':'1'}, {'front':'B','back':'2'}]
        answers = iter(['1','wrong'])
        printed = []
        score = study_cards(cards, input_fn=lambda prompt: next(answers), output_fn=printed.append)
        self.assertEqual(score, 1)
        self.assertTrue(any('1' in str(line) for line in printed))
    def test_study_empty(self):
        self.assertEqual(study_cards([], input_fn=lambda _: self.fail('Should not prompt'), output_fn=lambda _: None), 0)

if __name__ == '__main__':
    unittest.main()
