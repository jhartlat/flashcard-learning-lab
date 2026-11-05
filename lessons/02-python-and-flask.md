# Lesson 02 — From text files to the browser

This is an extension of Lesson 01. The original assignment still needs only the
standard library. Flask is needed for the web demo.

## Connect your work

Complete `student/flashcards.py` and run its original tests first. The web app
uses `demo_backend.py`, a separate reference implementation. Instructors should
know that this module contains solutions to parsing and normalization.

After your functions pass, change the import in `app.py` to:

```python
from student.flashcards import load_cards, check_answer
```

The browser does not call `study_cards`: JavaScript handles presentation while
Flask calls the same answer checker used by the terminal app.

## Method notebook

| Tool | Input → output | Example | Common mistake |
| --- | --- | --- | --- |
| `strip()` | string → string | `' hi '.strip()` → `'hi'` | Assuming it removes internal spaces |
| `lower()` | string → string | `'CPU'.lower()` → `'cpu'` | Not normalizing both answers |
| `split('|')` | string → list | `'Q|A'.split('|')` → `['Q', 'A']` | Indexing before validating length |
| `len()` | collection → integer | `len(['Q','A'])` → `2` | Confusing parts with characters |
| `append()` | mutates list; returns None | `cards.append(card)` | Assigning the return value to cards |
| `open()` | path → file object | `open(path, encoding='utf-8')` | Treating missing and empty files alike |
| `return` | function → caller | `return score` | Printing instead of returning |

Strings are immutable: string methods return new values. Lists are mutable:
append changes the existing list. Trace both values and types in your notes.

## Author a deck

`data/cards_part_two.txt` adds 36 Python and Flask cards. Each line must contain
exactly one `|`, with text on both sides. Do not put the delimiter inside a
question or answer, even inside quoted code. The example in Lesson 01 mentioning
`split('|')` cannot be stored as a card without rewording it: it has extra
separators. Use “Which method separates a string into a list of parts?” instead.

Keep answers concise. The checker ignores case and surrounding whitespace but
does not accept synonyms, punctuation changes, or internal-space changes.
For open-ended questions, reveal and compare your reasoning.

For each concept, write a definition card, an output-prediction card, and a
debugging prompt in your notes with an explanation.

## Follow one request

1. GET / loads deck names and counts.
2. GET /study/python renders a Jinja template and safely serializes the cards.
3. The browser displays one question and accepts an answer.
4. POST /api/check/python sends JSON such as `{"index": 0, "guess": "str"}`.
5. Flask validates the input, loads the deck, and checks the answer.
6. JSON returns to JavaScript, which updates feedback and the score.

Deck identifiers are allowlisted, so visitors cannot supply arbitrary file paths.
Jinja escapes text and JavaScript uses textContent to display answers. The cards
include their answers in browser data for reveal mode: this is a practice tool,
not a secure exam system.

## Session behavior

Correct answers add one point. Revealed or missed answers go into the review
list. Repeated button presses cannot score a card twice. Review starts a fresh
score for the missed cards. Reloading resets progress; nothing is saved to disk.

## Exercises

- Why must Flask validate the card index when JavaScript creates it?
- Explain why this app can work without a database.
- Predict outcomes for `Q|`, `Q|A|B`, and an empty file.
- Add three valid cards to Part Two and verify the deck count.
- Connect your completed student backend and rerun the web tests.

## References

- [Flask installation](https://flask.palletsprojects.com/en/stable/installation/)
- [Flask quickstart](https://flask.palletsprojects.com/en/stable/quickstart/)
- [Python string methods](https://docs.python.org/3/library/stdtypes.html#string-methods)
