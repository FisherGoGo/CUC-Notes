(function () {
  'use strict';

  const questions = globalThis.QUIZ_QUESTIONS;
  const core = globalThis.QuizCore;
  const root = document.getElementById('app-root');
  const liveStatus = document.getElementById('live-status');
  const STORAGE_KEY = 'cuc-computer-principles-quiz-v1';
  const CIRCLED = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨', '⑩'];

  if (!Array.isArray(questions) || !core || !root) {
    if (root) root.innerHTML = '<div class="empty-state"><h2>题库加载失败</h2><p>请重新打开完整的 HTML 文件。</p></div>';
    return;
  }

  const loaded = core.safeLoad(globalThis.localStorage, STORAGE_KEY, null);
  const state = {
    screen: 'home',
    mode: null,
    modeLabel: '',
    queue: [],
    index: 0,
    responses: {},
    records: loaded?.version === 1 && loaded.records ? loaded.records : {},
    storageAvailable: true,
  };

  function announce(message) {
    liveStatus.textContent = '';
    globalThis.setTimeout(() => {
      liveStatus.textContent = message;
    }, 10);
  }

  function persist() {
    state.storageAvailable = core.safeSave(globalThis.localStorage, STORAGE_KEY, {
      version: 1,
      records: state.records,
    });
  }

  function escapeHtml(value) {
    return String(value ?? '')
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#039;');
  }

  function renderInline(value) {
    return value
      .replace(/`([^`]+)`/g, '<code>$1</code>')
      .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
      .replace(/\$([^$\n]+)\$/g, '<span class="inline-math">$1</span>');
  }

  function renderMarkdown(markdown) {
    let source = String(markdown ?? '').replace(/\r\n/g, '\n');
    const blocks = [];
    const hold = (html) => {
      const token = `\u0000BLOCK${blocks.length}\u0000`;
      blocks.push(html);
      return token;
    };

    source = source.replace(/```([^\n]*)\n([\s\S]*?)```/g, (_match, language, code) => hold(
      `<pre data-language="${escapeHtml(language.trim())}"><code>${escapeHtml(code.trimEnd())}</code></pre>`,
    ));
    source = source.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, (_match, alt, url) => hold(
      `<img class="question-image" src="${escapeHtml(url)}" alt="${escapeHtml(alt)}">`,
    ));
    source = source.replace(/\$\$\s*([\s\S]*?)\s*\$\$/g, (_match, formula) => hold(
      `<div class="math-block" aria-label="公式">${escapeHtml(formula.trim())}</div>`,
    ));

    const escaped = escapeHtml(source);
    const html = escaped.split(/\n{2,}/).map((rawBlock) => {
      const block = rawBlock.trim();
      if (!block) return '';
      if (/^\u0000BLOCK\d+\u0000$/.test(block)) return block;
      const lines = block.split('\n');
      if (lines.every((line) => /^-\s+/.test(line))) {
        return `<ul>${lines.map((line) => `<li>${renderInline(line.replace(/^-\s+/, ''))}</li>`).join('')}</ul>`;
      }
      if (lines.every((line) => /^&gt;\s*/.test(line))) {
        return `<blockquote>${renderInline(lines.map((line) => line.replace(/^&gt;\s*/, '')).join('<br>'))}</blockquote>`;
      }
      return `<p>${renderInline(lines.join('<br>'))}</p>`;
    }).join('');

    return html.replace(/\u0000BLOCK(\d+)\u0000/g, (_match, index) => blocks[Number(index)]);
  }

  function typeName(type) {
    return { choice: '选择题', fill: '填空题', short: '简答题' }[type] ?? type;
  }

  function storageWarning() {
    return state.storageAvailable
      ? ''
      : '<p class="storage-warning" role="status">当前浏览器不允许保存本地数据，本次进度不会保留。</p>';
  }

  function renderHome() {
    state.screen = 'home';
    const stats = core.summarizeProgress(questions, state.records);
    root.innerHTML = `
      ${storageWarning()}
      <h2 class="screen-heading">今晚就把重点刷明白</h2>
      <p class="screen-intro">共 11 章、${stats.total} 道题。选择和填空自动判定，简答题对照参考答案自评。</p>
      <section class="stats-grid" aria-label="学习概览">
        <div class="stat"><span class="stat-value">${stats.total}</span><span class="stat-label">总题数</span></div>
        <div class="stat"><span class="stat-value">${stats.completed}</span><span class="stat-label">已完成</span></div>
        <div class="stat"><span class="stat-value">${stats.accuracy}%</span><span class="stat-label">客观题正确率</span></div>
        <div class="stat"><span class="stat-value">${stats.mistakes}</span><span class="stat-label">当前错题</span></div>
      </section>
      <section class="action-list" aria-label="练习方式">
        <div class="action-row">
          <div class="action-copy"><strong>按章节练习</strong><span>逐章推进，自动从未完成题目继续</span></div>
          <button class="btn-primary" data-action="show-chapters">选择章节</button>
        </div>
        <div class="action-row">
          <div class="action-copy"><strong>全题库随机</strong><span>本轮不重复，适合考前快速抽查</span></div>
          <div class="button-group">
            <label class="sr-only" for="random-count">随机题量</label>
            <select id="random-count" aria-label="随机题量">
              <option value="10">10 题</option>
              <option value="20" selected>20 题</option>
              <option value="30">30 题</option>
              <option value="50">50 题</option>
            </select>
            <button class="btn-primary" data-action="start-random">开始随机</button>
          </div>
        </div>
        <div class="action-row">
          <div class="action-copy"><strong>错题重练</strong><span>答对或标记掌握后自动移出错题</span></div>
          <button class="btn-secondary" data-action="start-mistakes" ${stats.mistakes ? '' : 'disabled'}>开始重练</button>
        </div>
        <div class="action-row">
          <div class="action-copy"><strong>清空进度</strong><span>删除本浏览器内的作答和错题记录</span></div>
          <button class="btn-danger" data-action="clear-progress" ${stats.completed ? '' : 'disabled'}>清空进度</button>
        </div>
      </section>`;
  }

  function renderChapters() {
    state.screen = 'chapters';
    const rows = [];
    for (let chapter = 1; chapter <= 11; chapter += 1) {
      const chapterQuestions = questions.filter((question) => question.chapter === chapter);
      const stats = core.summarizeProgress(chapterQuestions, state.records);
      rows.push(`
        <button class="chapter-row" data-action="start-chapter" data-chapter="${chapter}">
          <span class="chapter-copy"><strong>第 ${chapter} 章 · ${escapeHtml(chapterQuestions[0].chapterTitle)}</strong><span>${chapterQuestions.length} 道题</span></span>
          <span class="chapter-progress">${stats.completed} / ${stats.total}</span>
        </button>`);
    }

    root.innerHTML = `
      <div class="toolbar"><button class="btn-quiet" data-action="home">返回首页</button><span class="mode-label">选择章节</span></div>
      <h2 class="screen-heading">按章节练习</h2>
      <p class="screen-intro">点击章节后，从第一道未完成题开始。</p>
      <div class="chapter-list">${rows.join('')}</div>`;
  }

  function startQueue(queue, mode, modeLabel, startIndex = 0) {
    if (!queue.length) {
      root.innerHTML = '<div class="empty-state"><h2>这里暂时没有题目</h2><p>先完成一些练习，错题会出现在这里。</p><button class="btn-primary" data-action="home">返回首页</button></div>';
      return;
    }
    state.screen = 'question';
    state.mode = mode;
    state.modeLabel = modeLabel;
    state.queue = queue;
    state.index = Math.max(0, Math.min(startIndex, queue.length - 1));
    state.responses = {};
    renderQuestion();
  }

  function startChapter(chapter) {
    const queue = questions.filter((question) => question.chapter === chapter);
    startQueue(queue, 'chapter', `第 ${chapter} 章 · ${queue[0].chapterTitle}`, core.nextUnfinishedIndex(queue, state.records));
  }

  function startRandom() {
    const count = Number(document.getElementById('random-count')?.value ?? 20);
    startQueue(core.sampleWithoutReplacement(questions, count), 'random', `全题库随机 · ${count} 题`);
  }

  function startMistakes() {
    const queue = questions.filter((question) => state.records[question.id]?.mistake);
    startQueue(queue, 'mistakes', `错题重练 · ${queue.length} 题`);
  }

  function objectiveFeedback(question, response) {
    if (!response?.revealed) return '';
    const className = response.correct ? 'success' : 'error';
    const title = response.correct ? '回答正确' : '回答错误';
    const answerText = question.type === 'choice'
      ? question.answer
      : question.answer.map((answer, index) => `${CIRCLED[index]} ${answer}`).join('；');
    return `
      <div class="feedback ${className}" role="status">${title} · 参考答案：${escapeHtml(answerText)}</div>
      ${renderExplanation(question)}`;
  }

  function renderExplanation(question) {
    const parts = [];
    if (question.explanation) parts.push(`<h3>解析</h3><div class="markdown-body">${renderMarkdown(question.explanation)}</div>`);
    if (question.distractorAnalysis) parts.push(`<h3>选项分析</h3><div class="markdown-body">${renderMarkdown(question.distractorAnalysis)}</div>`);
    if (question.pitfall) parts.push(`<div class="pitfall"><strong>易错点：</strong>${renderMarkdown(question.pitfall)}</div>`);
    return parts.length ? `<div class="explanation">${parts.join('')}</div>` : '';
  }

  function renderChoice(question, response) {
    const options = question.options.map((option) => {
      const selected = response?.selected === option.key;
      let className = selected ? ' is-selected' : '';
      if (response?.revealed && option.key === question.answer) className += ' is-correct';
      if (response?.revealed && selected && option.key !== question.answer) className += ' is-wrong';
      return `
        <label class="option${className}">
          <input type="radio" name="choice" value="${escapeHtml(option.key)}" ${selected ? 'checked' : ''} ${response?.revealed ? 'disabled' : ''}>
          <span><strong>${escapeHtml(option.key)}.</strong> <span class="markdown-body">${renderMarkdown(option.text)}</span></span>
        </label>`;
    }).join('');
    return `<div class="option-list">${options}</div>${response?.revealed ? '' : '<button class="btn-primary" data-action="submit-choice">提交答案</button>'}${objectiveFeedback(question, response)}`;
  }

  function renderFill(question, response) {
    const fields = question.acceptedAnswers.map((_answers, index) => {
      const result = response?.results?.[index];
      const className = response?.revealed ? (result ? 'is-correct' : 'is-wrong') : '';
      return `
        <label class="fill-row"><strong>${CIRCLED[index]}</strong><input class="fill-answer ${className}" type="text" value="${escapeHtml(response?.values?.[index] ?? '')}" ${response?.revealed ? 'disabled' : ''} autocomplete="off"></label>`;
    }).join('');
    return `<div class="fill-list">${fields}</div>${response?.revealed ? '' : '<button class="btn-primary" data-action="submit-fill">提交答案</button>'}${objectiveFeedback(question, response)}`;
  }

  function renderShort(question, response) {
    const revealed = response?.revealed;
    const rating = response?.mastered;
    return `
      <label for="short-answer"><strong>先写下你的答案或要点</strong></label>
      <textarea id="short-answer" class="short-answer" ${revealed ? 'disabled' : ''} placeholder="在这里整理思路……">${escapeHtml(response?.draft ?? '')}</textarea>
      ${revealed ? '' : '<button class="btn-primary" data-action="reveal-short">查看参考答案</button>'}
      ${revealed ? `
        <div class="feedback info"><strong>参考答案</strong><div class="markdown-body">${renderMarkdown(question.answer)}</div></div>
        ${renderExplanation(question)}
        <div class="button-group" style="margin-top:16px">
          <button class="btn-secondary" data-action="rate-short" data-mastered="true" ${rating === true ? 'disabled' : ''}>掌握</button>
          <button class="btn-quiet" data-action="rate-short" data-mastered="false" ${rating === false ? 'disabled' : ''}>未掌握</button>
        </div>
        ${typeof rating === 'boolean' ? `<div class="feedback ${rating ? 'success' : 'error'}" role="status">已标记为${rating ? '掌握' : '未掌握'}</div>` : ''}` : ''}`;
  }

  function renderQuestion() {
    const question = state.queue[state.index];
    const response = state.responses[question.id];
    const progress = ((state.index + 1) / state.queue.length) * 100;
    let answerArea = '';
    if (question.type === 'choice') answerArea = renderChoice(question, response);
    if (question.type === 'fill') answerArea = renderFill(question, response);
    if (question.type === 'short') answerArea = renderShort(question, response);

    root.innerHTML = `
      <div class="question-shell">
        <div class="toolbar"><button class="btn-quiet" data-action="home">返回首页</button><span class="mode-label">${escapeHtml(state.modeLabel)}</span></div>
        <div class="question-meta">第 ${state.index + 1} / ${state.queue.length} 题</div>
        <div class="progress-track" aria-hidden="true"><div class="progress-bar" style="width:${progress}%"></div></div>
        <article class="question-card">
          <span class="type-tag">${typeName(question.type)} · 第 ${question.chapter} 章</span>
          <h2 class="question-title">${escapeHtml(question.title)}</h2>
          <div class="markdown-body">${renderMarkdown(question.prompt)}</div>
          <div class="answer-area">${answerArea}</div>
        </article>
        <nav class="question-actions" aria-label="题目导航">
          <button class="btn-quiet" data-action="previous" ${state.index === 0 ? 'disabled' : ''}>上一题</button>
          <button class="btn-primary" data-action="next">${state.index === state.queue.length - 1 ? '完成本轮' : '下一题'}</button>
        </nav>
      </div>`;
    globalThis.scrollTo({ top: 0, behavior: 'auto' });
  }

  function submitChoice() {
    const question = state.queue[state.index];
    const selected = root.querySelector('input[name="choice"]:checked')?.value;
    if (!selected) {
      announce('请先选择一个选项');
      return;
    }
    const correct = core.gradeChoice(selected, question.answer);
    state.responses[question.id] = { revealed: true, selected, correct };
    state.records[question.id] = core.updateRecord(state.records[question.id], { type: 'choice', correct });
    persist();
    renderQuestion();
    announce(correct ? '回答正确' : '回答错误');
  }

  function submitFill() {
    const question = state.queue[state.index];
    const values = [...root.querySelectorAll('.fill-answer')].map((input) => input.value);
    if (values.some((value) => !value.trim())) {
      announce('请填写所有空格');
      return;
    }
    const grading = core.gradeFill(values, question.acceptedAnswers);
    state.responses[question.id] = { revealed: true, values, ...grading };
    state.records[question.id] = core.updateRecord(state.records[question.id], { type: 'fill', correct: grading.correct });
    persist();
    renderQuestion();
    announce(grading.correct ? '回答正确' : '有空格填写错误');
  }

  function revealShort() {
    const question = state.queue[state.index];
    const draft = document.getElementById('short-answer')?.value ?? '';
    state.responses[question.id] = { revealed: true, draft };
    renderQuestion();
    announce('参考答案已显示，请自行判断掌握情况');
  }

  function rateShort(mastered) {
    const question = state.queue[state.index];
    state.responses[question.id] = { ...state.responses[question.id], mastered };
    state.records[question.id] = core.updateRecord(state.records[question.id], { type: 'short', mastered });
    persist();
    renderQuestion();
    announce(mastered ? '已标记为掌握' : '已加入错题重练');
  }

  function renderSummary() {
    state.screen = 'summary';
    const stats = core.summarizeProgress(state.queue, state.records);
    root.innerHTML = `
      <div class="summary-card">
        <h2>本轮完成</h2>
        <p>共 ${stats.total} 题，已完成 ${stats.completed} 题；客观题正确率 ${stats.accuracy}%，当前仍有 ${stats.mistakes} 道需要重练。</p>
        <div class="button-group">
          <button class="btn-primary" data-action="home">返回首页</button>
          ${stats.mistakes ? '<button class="btn-secondary" data-action="start-mistakes">错题重练</button>' : ''}
        </div>
      </div>`;
  }

  function move(delta) {
    const next = state.index + delta;
    if (next >= state.queue.length) {
      renderSummary();
      return;
    }
    state.index = Math.max(0, next);
    renderQuestion();
  }

  root.addEventListener('click', (event) => {
    const button = event.target.closest('[data-action]');
    if (!button || button.disabled) return;
    const { action } = button.dataset;

    if (action === 'home') renderHome();
    if (action === 'show-chapters') renderChapters();
    if (action === 'start-chapter') startChapter(Number(button.dataset.chapter));
    if (action === 'start-random') startRandom();
    if (action === 'start-mistakes') startMistakes();
    if (action === 'submit-choice') submitChoice();
    if (action === 'submit-fill') submitFill();
    if (action === 'reveal-short') revealShort();
    if (action === 'rate-short') rateShort(button.dataset.mastered === 'true');
    if (action === 'previous') move(-1);
    if (action === 'next') move(1);
    if (action === 'clear-progress') {
      if (globalThis.confirm('确定清空全部刷题进度和错题记录吗？')) {
        state.records = {};
        persist();
        renderHome();
        announce('进度已清空');
      }
    }
  });

  persist();
  renderHome();
})();
