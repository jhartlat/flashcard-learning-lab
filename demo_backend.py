"""Working web demo. Student exercises remain in student/flashcards.py.

Instructors: this module contains a reference parser and answer checker.
After completing Lesson 01, switch the imports in app.py to your student code.
"""
from pathlib import Path


def parse_card(line):
    parts = line.strip().split('|')
    if len(parts) != 2 or not all(part.strip() for part in parts):
        return None
    return dict(zip(('front', 'back'), (part.strip() for part in parts)))


def load_cards(filename):
    with Path(filename).open(encoding='utf-8') as source:
        return [card for line in source if (card := parse_card(line)) is not None]


def check_answer(guess, answer):
    return guess.strip().lower() == answer.strip().lower()
