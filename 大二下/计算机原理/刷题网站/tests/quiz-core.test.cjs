const test = require('node:test');
const assert = require('node:assert/strict');

const {
  gradeChoice,
  gradeFill,
  nextUnfinishedIndex,
  normalizeAnswer,
  safeLoad,
  safeSave,
  sampleWithoutReplacement,
  summarizeProgress,
  updateRecord,
} = require('../quiz-core.js');

test('normalizes case, width, whitespace, markdown ticks, and punctuation', () => {
  assert.equal(normalizeAnswer(' `１２００　Baud；` '), '1200baud');
});

test('grades a single choice answer', () => {
  assert.equal(gradeChoice('b', 'B'), true);
  assert.equal(gradeChoice('A', 'B'), false);
});

test('grades every fill against accepted alternatives', () => {
  assert.deepEqual(
    gradeFill(
      [' 加速图形接口 ', '图形接口'],
      [
        ['加速图形端口', '加速图形接口'],
        ['总线接口', '图形接口'],
      ],
    ),
    { correct: true, results: [true, true] },
  );
  assert.deepEqual(
    gradeFill(['错误', '图形接口'], [['正确'], ['图形接口']]),
    { correct: false, results: [false, true] },
  );
});

test('samples without repetition and clamps the requested count', () => {
  const items = ['a', 'b', 'c'];
  assert.deepEqual(sampleWithoutReplacement(items, 99, () => 0), ['b', 'c', 'a']);
  assert.equal(new Set(sampleWithoutReplacement(items, 2, () => 0.5)).size, 2);
  assert.deepEqual(items, ['a', 'b', 'c']);
});

test('finds the first unfinished question', () => {
  const queue = [{ id: 'a' }, { id: 'b' }, { id: 'c' }];
  assert.equal(nextUnfinishedIndex(queue, { a: { completed: true } }), 1);
  assert.equal(nextUnfinishedIndex(queue, { a: { completed: true }, b: { completed: true }, c: { completed: true } }), 0);
});

test('updates objective and short-answer records', () => {
  const wrong = updateRecord(undefined, { type: 'choice', correct: false });
  assert.equal(wrong.attempts, 1);
  assert.equal(wrong.completed, true);
  assert.equal(wrong.mistake, true);

  const corrected = updateRecord(wrong, { type: 'choice', correct: true });
  assert.equal(corrected.attempts, 2);
  assert.equal(corrected.mistake, false);

  const unmastered = updateRecord(undefined, { type: 'short', mastered: false });
  assert.equal(unmastered.mistake, true);
  assert.equal(unmastered.mastered, false);
});

test('summarizes completion, objective accuracy, and mistakes', () => {
  const questions = [
    { id: 'a', type: 'choice' },
    { id: 'b', type: 'fill' },
    { id: 'c', type: 'short' },
  ];
  const records = {
    a: { completed: true, correct: true, mistake: false },
    b: { completed: true, correct: false, mistake: true },
    c: { completed: true, mastered: false, mistake: true },
  };

  assert.deepEqual(summarizeProgress(questions, records), {
    total: 3,
    completed: 3,
    objectiveAttempted: 2,
    objectiveCorrect: 1,
    accuracy: 50,
    mistakes: 2,
  });
});

test('loads and saves storage without breaking when storage is unavailable', () => {
  const memory = new Map();
  const storage = {
    getItem: (key) => memory.get(key) ?? null,
    setItem: (key, value) => memory.set(key, value),
  };

  assert.equal(safeSave(storage, 'state', { answer: 42 }), true);
  assert.deepEqual(safeLoad(storage, 'state', {}), { answer: 42 });
  memory.set('broken', '{bad json');
  assert.deepEqual(safeLoad(storage, 'broken', { reset: true }), { reset: true });

  const denied = {
    getItem: () => { throw new Error('denied'); },
    setItem: () => { throw new Error('denied'); },
  };
  assert.deepEqual(safeLoad(denied, 'state', { fallback: true }), { fallback: true });
  assert.equal(safeSave(denied, 'state', {}), false);
});
