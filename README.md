# Flashcard Learning Lab

A beginner-first Python tutorial with a working Flask study interface. Study two
decks (39 cards), check answers, reveal answers, and revisit missed cards.

## Quick start

Install Python 3.10 or newer. Open a terminal in this folder.

Windows PowerShell (no activation or execution-policy changes required):

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m flask --app app run
```

macOS / Linux:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m flask --app app run
```

Open http://127.0.0.1:5000. Stop with Ctrl+C. If the port is busy, add `--port 5001`.
No Node.js, database, account, API key, or external fonts are required.
Flask and its transitive dependencies are installed by requirements.txt.
The Flask development server is for local learning, not public hosting.

## Learning sequence

1. Read lessons/01-flashcards.md and implement student/flashcards.py.
2. Record method definitions, examples, types, and observations in NOTES_TEMPLATE.md.
3. Run the original assignment tests; they fail until the student functions are completed.
4. Explore lessons/02-python-and-flask.md and data/cards_part_two.txt.
5. Connect your completed functions by changing the import in app.py from
   `demo_backend` to `student.flashcards`.

The working web app uses demo_backend.py. The original student stubs, tests, and
starter deck are unchanged. Instructor note: the demo backend contains reference
solutions for parsing, loading, and checking. Share a student-only copy if you
want learners to solve those functions without seeing solutions.

## Tests

Windows commands (use .venv/bin/python on macOS/Linux):

```powershell
# Working demo and web routes: expected to pass.
.\.venv\Scripts\python.exe -m unittest discover -s web_tests -v
# Original assignment: intentionally fails until students complete it.
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

unittest comes with Python; no extra test package is required.

## Study behavior

- Answers ignore capitalization and surrounding whitespace; otherwise they match exactly.
- Reveals count as practice, not correct answers. Retry targets only missed cards.
- Progress stays in the current tab and resets on refresh or navigation.
- Answers are in browser data for reveal mode; this is self-study, not a secure exam.
- Edit decks as UTF-8 with exactly one delimiter per line: question|answer.
  Empty or malformed lines are skipped. See Lesson 02 for delimiter limitations.

## Project map

| Path | Purpose |
| --- | --- |
| app.py | Flask routes and request validation |
| demo_backend.py | Working reference parser and checker |
| templates/, static/ | Responsive UI, styles, and study interactions |
| student/flashcards.py | Original unfinished assignment |
| tests/ | Original assignment tests, unchanged |
| web_tests/ | Demo backend and HTTP tests |
| data/cards.txt | Original three-card fixture |
| data/cards_part_two.txt | 36 new Python and Flask cards |
| lessons/ | Guided lessons and method notes |

## Publish your own copy

The .gitignore excludes virtual environments, caches, and .env files. Create an
empty repository in your own account, review the files, then run:

```sh
git init
git add .
git commit -m "Add Flask learning lab and expanded tutorial"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace the URL with your repository. GitHub publishing does not host the Flask
server. See the [official Flask installation guide](https://flask.palletsprojects.com/en/stable/installation/).
