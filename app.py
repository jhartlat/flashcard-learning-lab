"""Local classroom web app: python -m flask --app app run."""
from pathlib import Path

from flask import Flask, abort, jsonify, render_template, request
from demo_backend import load_cards, check_answer

ROOT = Path(__file__).resolve().parent
DECKS = {
    'starter': {'title': 'The warm-up', 'description': 'Three quick questions to learn the flow.', 'file': 'cards.txt', 'tag': 'START HERE'},
    'python': {'title': 'Python, piece by piece', 'description': 'Strings, files, functions, and the journey from notes to code.', 'file': 'cards_part_two.txt', 'tag': 'PART TWO'},
}


def create_app():
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 8192

    def cards_for(deck):
        if deck not in DECKS:
            abort(404)
        return load_cards(ROOT / 'data' / DECKS[deck]['file'])

    @app.get('/')
    def home():
        decks = [dict(info, id=key, count=len(cards_for(key))) for key, info in DECKS.items()]
        return render_template('index.html', decks=decks)

    @app.get('/study/<deck>')
    def study(deck):
        cards = cards_for(deck)
        return render_template('study.html', deck=DECKS[deck], deck_id=deck, cards=cards)

    @app.post('/api/check/<deck>')
    def check(deck):
        cards = cards_for(deck)
        payload = request.get_json(silent=True)
        if not isinstance(payload, dict):
            abort(400)
        index, guess = payload.get('index'), payload.get('guess')
        if type(index) is not int or not 0 <= index < len(cards) or not isinstance(guess, str) or len(guess) > 2000:
            abort(400)
        return jsonify(correct=check_answer(guess, cards[index]['back']), answer=cards[index]['back'])

    @app.get('/notes')
    def notes():
        return render_template('notes.html')

    @app.errorhandler(404)
    def not_found(error):
        return render_template('error.html'), 404

    return app


app = create_app()
