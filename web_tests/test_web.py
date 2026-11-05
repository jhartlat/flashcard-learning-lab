"""Tests for the working demo; the original assignment suite is separate."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app import create_app, DECKS, ROOT
from demo_backend import parse_card, load_cards, check_answer


class DemoTests(unittest.TestCase):
    def test_parser_and_malformed_lines(self):
        self.assertEqual(parse_card(' Q | A \n'), {'front': 'Q', 'back': 'A'})
        for line in ('', 'Q', 'Q|', '|A', 'Q|A|B', ' | '):
            with self.subTest(line=line):
                self.assertIsNone(parse_card(line))

    def test_file_filter_order_and_empty(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'cards.txt'
            path.write_text('A|1\ninvalid\nB|2\n', encoding='utf-8')
            self.assertEqual(load_cards(path), [{'front': 'A', 'back': '1'}, {'front': 'B', 'back': '2'}])
            path.write_text('', encoding='utf-8')
            self.assertEqual(load_cards(path), [])

    def test_normalization(self):
        self.assertTrue(check_answer(' PARIS ', 'paris'))
        self.assertFalse(check_answer('london', 'paris'))

    def test_all_shipped_cards_valid(self):
        for deck in DECKS.values():
            lines = (ROOT / 'data' / deck['file']).read_text(encoding='utf-8').splitlines()
            self.assertTrue(lines)
            self.assertTrue(all(parse_card(line) is not None for line in lines))
        self.assertEqual(len(load_cards(ROOT / 'data/cards_part_two.txt')), 36)


class WebTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.client = self.app.test_client()

    def test_pages_and_assets(self):
        for path in ('/', '/notes', '/study/starter', '/study/python', '/static/style.css', '/static/study.js'):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                response.close()
        self.assertIn(b'36 cards', self.client.get('/').data)

    def test_correct_and_incorrect_answers(self):
        good = self.client.post('/api/check/starter', json={'index': 1, 'guess': ' 4 '})
        self.assertEqual(good.json, {'correct': True, 'answer': '4'})
        bad = self.client.post('/api/check/starter', json={'index': 1, 'guess': '5'})
        self.assertFalse(bad.json['correct'])

    def test_reject_bad_payloads(self):
        for payload in ([], None, {}, {'index': -1, 'guess': 'x'}, {'index': 999, 'guess': 'x'},
                        {'index': True, 'guess': 'x'}, {'index': '1', 'guess': 'x'},
                        {'index': 0, 'guess': 4}, {'index': 0, 'guess': 'a' * 2001}):
            with self.subTest(payload=payload):
                self.assertEqual(self.client.post('/api/check/starter', json=payload).status_code, 400)
        self.assertEqual(self.client.post('/api/check/starter', data='broken', content_type='application/json').status_code, 400)

    def test_unknown_deck(self):
        self.assertEqual(self.client.get('/study/unknown').status_code, 404)
        self.assertEqual(self.client.post('/api/check/unknown', json={}).status_code, 404)
        self.assertEqual(self.client.get('/missing').status_code, 404)

    def test_empty_deck(self):
        with patch('app.load_cards', return_value=[]):
            self.assertIn(b'waiting for cards', self.client.get('/study/starter').data)
            self.assertEqual(self.client.post('/api/check/starter', json={'index': 0, 'guess': 'x'}).status_code, 400)

    def test_card_content_cannot_close_script(self):
        with patch('app.load_cards', return_value=[{'front': '</script><script>alert(1)</script>', 'back': 'a'}]):
            page = self.client.get('/study/starter').data
            self.assertNotIn(b'<script>alert(1)</script>', page)
            self.assertIn(b'\\u003c', page)

    def test_size_limit(self):
        self.assertEqual(self.client.post('/api/check/starter', data='x' * 9000, content_type='application/json').status_code, 413)


if __name__ == '__main__':
    unittest.main()
