(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  root.QuizCore = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  function normalizeAnswer(value) {
    return String(value ?? '')
      .normalize('NFKC')
      .toLowerCase()
      .replaceAll('`', '')
      .replace(/\s+/g, '')
      .replace(/[；;，,。.!！、:：]/g, '');
  }

  function gradeChoice(selected, answer) {
    return String(selected ?? '').trim().toUpperCase()
      === String(answer ?? '').trim().toUpperCase();
  }

  function gradeFill(values, acceptedAnswers) {
    const results = acceptedAnswers.map((alternatives, index) => {
      const candidate = normalizeAnswer(values[index]);
      return candidate.length > 0 && alternatives.some(
        (alternative) => normalizeAnswer(alternative) === candidate,
      );
    });
    return {
      correct: results.length > 0 && results.every(Boolean),
      results,
    };
  }

  function sampleWithoutReplacement(items, requestedCount, random = Math.random) {
    const copy = [...items];
    for (let index = copy.length - 1; index > 0; index -= 1) {
      const target = Math.floor(random() * (index + 1));
      [copy[index], copy[target]] = [copy[target], copy[index]];
    }
    const count = Math.max(0, Math.min(copy.length, Number(requestedCount) || 0));
    return copy.slice(0, count);
  }

  function nextUnfinishedIndex(queue, records) {
    const index = queue.findIndex((question) => !records[question.id]?.completed);
    return index === -1 ? 0 : index;
  }

  function updateRecord(existing, result) {
    const previous = existing ?? {};
    const isShort = result.type === 'short';
    const correct = isShort ? null : Boolean(result.correct);
    const mastered = isShort ? Boolean(result.mastered) : null;
    return {
      ...previous,
      attempts: (previous.attempts ?? 0) + 1,
      completed: true,
      correct,
      mastered,
      mistake: isShort ? !mastered : !correct,
      updatedAt: new Date().toISOString(),
    };
  }

  function summarizeProgress(questions, records) {
    let completed = 0;
    let objectiveAttempted = 0;
    let objectiveCorrect = 0;
    let mistakes = 0;

    for (const question of questions) {
      const record = records[question.id];
      if (!record) continue;
      if (record.completed) completed += 1;
      if (record.mistake) mistakes += 1;
      if (question.type !== 'short' && record.completed) {
        objectiveAttempted += 1;
        if (record.correct) objectiveCorrect += 1;
      }
    }

    return {
      total: questions.length,
      completed,
      objectiveAttempted,
      objectiveCorrect,
      accuracy: objectiveAttempted
        ? Math.round((objectiveCorrect / objectiveAttempted) * 100)
        : 0,
      mistakes,
    };
  }

  function safeLoad(storage, key, fallback) {
    try {
      const value = storage?.getItem(key);
      return value ? JSON.parse(value) : fallback;
    } catch {
      return fallback;
    }
  }

  function safeSave(storage, key, value) {
    try {
      storage?.setItem(key, JSON.stringify(value));
      return Boolean(storage);
    } catch {
      return false;
    }
  }

  return Object.freeze({
    gradeChoice,
    gradeFill,
    nextUnfinishedIndex,
    normalizeAnswer,
    safeLoad,
    safeSave,
    sampleWithoutReplacement,
    summarizeProgress,
    updateRecord,
  });
});
