'use strict';
const shell = document.querySelector('#study');
if (shell) {
  const cards = JSON.parse(document.querySelector('#cards-data').textContent);
  const $ = (id) => document.getElementById(id);
  let queue = cards.map((_, index) => index), position = 0, correct = 0, missed = [], answered = false, busy = false;
  function showCard() {
    answered = false;
    $('question').textContent = cards[queue[position]].front;
    $('position').textContent = `Card ${position + 1} of ${queue.length}`;
    $('score').textContent = `${correct} correct`;
    $('progress').max = queue.length;
    $('progress').value = position;
    $('answer-form').hidden = false;
    $('answer-form').reset();
    $('feedback').hidden = true;
    $('next').hidden = true;
    $('question').focus();
  }
  function finishCard(isCorrect, answer, revealed) {
    if (answered) return;
    answered = true;
    if (isCorrect) correct++; else missed.push(queue[position]);
    $('answer-form').hidden = true;
    $('feedback').hidden = false;
    $('feedback').className = isCorrect ? 'feedback success' : 'feedback practice';
    const title = document.createElement('strong');
    title.textContent = isCorrect ? 'You got it.' : revealed ? 'A little more practice.' : 'Keep learning.';
    const detail = document.createElement('p');
    detail.textContent = `Answer: ${answer}`;
    $('feedback').replaceChildren(title, detail);
    $('score').textContent = `${correct} correct`;
    $('progress').value = position + 1;
    $('next').textContent = position + 1 === queue.length ? 'See your results →' : 'Next card →';
    $('next').hidden = false;
    $('next').focus();
  }
  $('answer-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    if (busy || answered) return;
    if (!$('guess').value.trim()) { $('guess').focus(); return; }
    busy = true;
    const controls = [...$('answer-form').querySelectorAll('button')];
    controls.forEach(button => button.disabled = true);
    try {
      const response = await fetch(shell.dataset.checkUrl, {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({index: queue[position], guess: $('guess').value})
      });
      if (!response.ok) throw new Error('Unable to check');
      const result = await response.json();
      finishCard(result.correct, result.answer, false);
    } catch (error) {
      $('feedback').className = 'feedback practice';
      $('feedback').textContent = 'Could not reach the app. Your answer is still here. Check that Flask is running and try again.';
      $('feedback').hidden = false;
    } finally {
      busy = false;
      controls.forEach(button => button.disabled = false);
    }
  });
  $('reveal').addEventListener('click', () => {
    if (!busy) finishCard(false, cards[queue[position]].back, true);
  });
  $('next').addEventListener('click', () => {
    if (!answered) return;
    position++;
    if (position < queue.length) { showCard(); return; }
    shell.hidden = true;
    $('results').hidden = false;
    $('result-score').textContent = `${correct} / ${queue.length} correct`;
    $('result-copy').textContent = missed.length ? `${missed.length} cards to revisit. A second pass helps the ideas settle in.` : 'Every answer recalled. Nice work—try explaining each idea in your own words.';
    $('retry').hidden = missed.length === 0;
    $('results').tabIndex = -1;
    $('results').focus();
  });
  $('retry').addEventListener('click', () => {
    queue = [...missed]; position = 0; correct = 0; missed = [];
    $('results').hidden = true; shell.hidden = false; showCard();
  });
  showCard();
}
