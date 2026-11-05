# Lesson 01 — Build a file-based flashcard study tool

## Goal and scope
Create a terminal flashcard program. You receive `data/cards.txt` containing `front|back` lines. You must not hardcode cards, use databases, install packages, or modify the supplied tests. Invalid lines are skipped. The program must preserve card order, compare answers without case sensitivity, and return a score.

## First: trace the data
```
Raw file line:   'What is 2 + 2?|4\n'              (str)
Clean line:      'What is 2 + 2?|4'                (str)
Split parts:     ['What is 2 + 2?', '4']           (list[str])
Validated card:  {'front':'What is 2 + 2?', 'back':'4'} (dict)
Loaded cards:    [{'front':..., 'back':...}, ...]   (list[dict])
Student answer:  ' 4 '                           (str)
Answer result:   True                            (bool)
Study score:     1                               (int)
```

## Function contracts: input → toolkit → output

### `parse_card(line)`
**Input:** `'  What is 2 + 2? | 4 \n'` (one string)

**Methods you may use:**
- `str.strip()` removes surrounding whitespace: `' hello \n'.strip()` → `'hello'`.
- `str.split('|')` creates a list: `'a|b'.split('|')` → `['a', 'b']`.
- `len(parts)` counts parts: `len(['a','b'])` → `2`.
- `if` checks conditions: `if len(parts) != 2:` means the line is malformed.
- List indexing: `parts[0]` is the front, `parts[1]` is the back (only after validating length).
- Dictionary literals: `{'front':'a','back':'b'}` label the two values.
- `return None` signals invalid data.

**Output:** `{'front':'What is 2 + 2?', 'back':'4'}`. For `broken`, `|answer`, `question|`, or `a|b|c`, output `None`.

**Your task:** decide the order of cleaning, splitting, checking, and constructing. Do not index before checking the list length.

### `load_cards(filename)`
**Input:** `'data/cards.txt'` (file path string)

**Methods you may use:**
- `with open(filename, 'r', encoding='utf-8') as file:` safely opens a file.
- `for line in file:` visits one line at a time.
- `parse_card(line)` reuses your first function.
- `if card is not None:` keeps valid cards.
- `cards.append(card)` adds an item to a list: `[1].append(2)` changes the list to `[1, 2]`.

**Output:** `[{'front':'What does CPU stand for?', 'back':'Central Processing Unit'}, ...]`.

**Your task:** initialize a list, open the file, transform each line, filter invalid cards, and return the list. An empty file returns `[]`. A missing file may raise `FileNotFoundError`.

### `check_answer(guess, answer)`
**Input:** `'  PARIS '` and `'paris'` (two strings)

**Methods you may use:**
- `str.strip()` removes whitespace around each string.
- `str.lower()` normalizes capitalization: `'PyThOn'.lower()` → `'python'`.
- `==` compares two strings and produces `True` or `False`.

**Output:** `True`. `'London'` vs `'Paris'` returns `False`.

**Your task:** normalize both values before comparison.

### `study_cards(cards, input_fn=input, output_fn=print)`
**Input:** `[{'front':'2 + 2?', 'back':'4'}]` (list of dictionaries)

**Methods you may use:**
- `for card in cards:` iterates over cards.
- `card['front']` and `card['back']` retrieve dictionary values.
- `input_fn('Answer: ')` obtains a response; tests can substitute a fake input function.
- `output_fn('Correct!')` displays feedback; tests can capture it.
- `check_answer(guess, answer)` evaluates a response.
- `score += 1` increments a number.

**Output:** `1` (integer score when the response was correct). Also display question and correctness feedback. Empty input list returns `0` without asking anything.

**Your task:** connect presentation, response, evaluation, and scoring without duplicating comparison logic.

## Implementation steps
1. Predict the type and value after each transformation in the data trace; write it in your notes.
2. Implement `parse_card` and run tests. Fix malformed-line cases before proceeding.
3. Implement `load_cards` and test empty files and invalid lines.
4. Implement `check_answer` and test capitalization and whitespace.
5. Implement `study_cards`, run all tests, and explain why fake input/output functions make testing easier.

## Tests and expected outcomes
From repository root: `python -m unittest discover -s tests -v`.
The starter intentionally fails tests until you implement the functions. Do not change tests to force a pass. A passing test proves a specific example behaves as specified, not that every possible input is correct.

## Notes → flashcards → quiz
Write notes for each function: its responsibility, input type, output type, failure behavior, and data transformation. Make three study flashcards per function: **definition**, **predict the output**, and **debug a mistake**. Example: `What does split('|') return for 'a|b'?|['a', 'b']`. Then write a five-question quiz testing parsing, validation, data structures, function responsibilities, and output prediction. Add your cards to a separate notes file; do not change the provided assignment fixture.

## Reflection
Why validate before indexing? Why does `load_cards` call `parse_card`? What happens to the output type if a line is invalid? Which tests would catch accidentally returning a string instead of a dictionary? What is different between printing a score and returning a score?
