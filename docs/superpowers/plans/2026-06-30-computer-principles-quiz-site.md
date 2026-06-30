# Computer Principles Offline Quiz Site Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a zero-dependency offline static quiz website from the 11 answered computer-principles Markdown question banks, excluding the six approved programming questions.

**Architecture:** A Node-only development script parses the source Markdown into a browser-ready `questions.js`; users only receive a classic-script static site that runs over `file://`. Pure quiz rules live in a UMD-style `quiz-core.js` so the same functions run in the browser and Node's built-in test runner, while `app.js` owns DOM rendering and local persistence.

**Tech Stack:** HTML5, CSS3, vanilla JavaScript, Node.js 22 built-in test runner, PowerShell for local asset copying.

---

## File map

- Create `大二下/计算机原理/刷题网站/index.html`: semantic shell and stable DOM targets.
- Create `大二下/计算机原理/刷题网站/styles.css`: practical responsive design and state styles.
- Create `大二下/计算机原理/刷题网站/quiz-core.js`: pure normalization, grading, sampling, statistics, and storage helpers.
- Create `大二下/计算机原理/刷题网站/app.js`: screen routing, rendering, events, and persistence orchestration.
- Generate `大二下/计算机原理/刷题网站/questions.js`: browser-ready question data.
- Create `大二下/计算机原理/刷题网站/scripts/question-parser.mjs`: source Markdown parser and validation.
- Create `大二下/计算机原理/刷题网站/scripts/build-questions.mjs`: reads all 11 sources and writes `questions.js`.
- Create `大二下/计算机原理/刷题网站/tests/question-parser.test.mjs`: parser and source-data tests.
- Create `大二下/计算机原理/刷题网站/tests/quiz-core.test.cjs`: pure quiz behavior tests.
- Create `大二下/计算机原理/刷题网站/tests/static-site.test.mjs`: offline shell and asset contract tests.
- Create `大二下/计算机原理/刷题网站/assets/5-13.png`, `5-15.png`, and `9-12.png`: retained local question images.
- Create `大二下/计算机原理/刷题网站/README.md`: opening, sharing, testing, and reset instructions.

### Task 1: Parse and classify the answered Markdown banks

**Files:**
- Create: `大二下/计算机原理/刷题网站/tests/question-parser.test.mjs`
- Create: `大二下/计算机原理/刷题网站/scripts/question-parser.mjs`

- [ ] **Step 1: Write failing parser tests**

Cover one choice question, one multi-blank fill question, one short-answer question, Markdown image rewriting, and explicit exclusions:

```js
import test from 'node:test';
import assert from 'node:assert/strict';
import { parseChapter, shouldExclude } from '../scripts/question-parser.mjs';

test('parses a choice question with answer and explanation', () => {
  const questions = parseChapter('# 第一章练习题\n\n## 1. 总线\n\n**题目：** 数据总线用于（ ）。\n\n**选项：**\n\n- A. 寻址\n- B. 传数据\n\n**答案：B**\n\n**解析：** 数据总线传数据。', 1);
  assert.equal(questions[0].type, 'choice');
  assert.deepEqual(questions[0].options, [{ key: 'A', text: '寻址' }, { key: 'B', text: '传数据' }]);
  assert.equal(questions[0].answer, 'B');
});

test('parses numbered blanks in order', () => {
  const questions = parseChapter('# 第十一章练习题\n\n## 9. 总线分类\n\n**题目：** ① 位于芯片内部，② 位于系统之间。\n\n**答案：** ① 片内总线 ② 外总线\n\n**解析：** 按范围分类。', 11);
  assert.equal(questions[0].type, 'fill');
  assert.deepEqual(questions[0].answer, ['片内总线', '外总线']);
});

test('classifies prose answers as short answer', () => {
  const questions = parseChapter('# 第六章练习题\n\n## 21. 中断过程\n\n**题目：** 简述中断处理过程。\n\n**答案：** 请求、响应、保护现场、服务、恢复和返回。\n\n**解析：** 按处理顺序作答。', 6);
  assert.equal(questions[0].type, 'short');
});

test('rewrites retained source images to local assets', () => {
  const questions = parseChapter('# 第九章练习题\n\n## 12. 连接图\n\n**题目：** 根据下图判断。\n\n![图](../assets/9-12.png)\n\n**答案：** 方式 2。', 9);
  assert.match(questions[0].prompt, /assets\/9-12\.png/);
});

test('excludes only the six approved programming questions', () => {
  assert.equal(shouldExclude(4, 14), true);
  assert.equal(shouldExclude(7, 17), true);
  assert.equal(shouldExclude(7, 18), true);
  assert.equal(shouldExclude(7, 19), true);
  assert.equal(shouldExclude(9, 10), true);
  assert.equal(shouldExclude(9, 11), true);
  assert.equal(shouldExclude(9, 12), false);
});
```

- [ ] **Step 2: Run tests and verify RED**

Run from `大二下/计算机原理/刷题网站`:

```powershell
node --test tests/question-parser.test.mjs
```

Expected: FAIL because `scripts/question-parser.mjs` does not exist.

- [ ] **Step 3: Implement the minimal parser**

Implement exported `parseChapter(markdown, chapterNumber)`, `parseQuestionSection(section, chapterNumber)`, `extractNumberedAnswers(text)`, `rewriteAssetPaths(markdown)`, and `shouldExclude(chapter, sourceNumber)`. Split question sections on `^## <number>.`, derive stable IDs with `chNN-qNN`, and retain `题目`, options, answer, analysis, distractor analysis, and pitfall blocks.

- [ ] **Step 4: Run tests and verify GREEN**

```powershell
node --test tests/question-parser.test.mjs
```

Expected: all parser tests PASS with no warnings.

- [ ] **Step 5: Commit parser slice**

```powershell
git add -- '大二下/计算机原理/刷题网站/scripts/question-parser.mjs' '大二下/计算机原理/刷题网站/tests/question-parser.test.mjs'
git commit -m "feat: parse computer principles question banks"
```

### Task 2: Generate and validate the complete browser question data

**Files:**
- Modify: `大二下/计算机原理/刷题网站/tests/question-parser.test.mjs`
- Create: `大二下/计算机原理/刷题网站/scripts/build-questions.mjs`
- Generate: `大二下/计算机原理/刷题网站/questions.js`
- Create: `大二下/计算机原理/刷题网站/assets/5-13.png`
- Create: `大二下/计算机原理/刷题网站/assets/5-15.png`
- Create: `大二下/计算机原理/刷题网站/assets/9-12.png`

- [ ] **Step 1: Add failing full-bank validation tests**

Read all 11 source files, parse them, and assert: chapters 1–11 exist; IDs are unique; every choice answer matches an option; every fill answer count matches its circled blanks; no excluded ID exists; every referenced asset belongs to the three retained files; all questions have prompt and answer content.

- [ ] **Step 2: Run the validation test and verify RED**

```powershell
node --test tests/question-parser.test.mjs
```

Expected: FAIL on any parser edge case surfaced by the real banks.

- [ ] **Step 3: Refine parsing and add the build script**

The build script must:

```js
const banner = `/* Generated from the answered Markdown banks. Do not edit by hand. */`;
const output = `${banner}\n(function (root) {\n  const questions = ${JSON.stringify(questions, null, 2)};\n  root.QUIZ_QUESTIONS = questions;\n  if (typeof module === 'object' && module.exports) module.exports = questions;\n})(typeof globalThis !== 'undefined' ? globalThis : this);\n`;
```

Write UTF-8 output to `questions.js`, then copy only `5-13.png`, `5-15.png`, and `9-12.png` from the course assets directory.

- [ ] **Step 4: Build and verify GREEN**

```powershell
node scripts/build-questions.mjs
node --test tests/question-parser.test.mjs
```

Expected: build reports total and per-type counts; all tests PASS.

- [ ] **Step 5: Commit generated data slice**

```powershell
git add -- '大二下/计算机原理/刷题网站/questions.js' '大二下/计算机原理/刷题网站/assets' '大二下/计算机原理/刷题网站/scripts' '大二下/计算机原理/刷题网站/tests/question-parser.test.mjs'
git commit -m "feat: generate offline computer principles quiz data"
```

### Task 3: Implement pure grading, sampling, progress, and storage rules

**Files:**
- Create: `大二下/计算机原理/刷题网站/tests/quiz-core.test.cjs`
- Create: `大二下/计算机原理/刷题网站/quiz-core.js`

- [ ] **Step 1: Write failing core behavior tests**

Test `normalizeAnswer`, `gradeChoice`, `gradeFill`, `sampleWithoutReplacement`, `summarizeProgress`, `nextUnfinishedIndex`, `updateRecord`, `safeLoad`, and `safeSave`. Include whitespace, ASCII/full-width punctuation, case-insensitive text, synonyms, random uniqueness, malformed storage JSON, and simple storage denial.

- [ ] **Step 2: Run tests and verify RED**

```powershell
node --test tests/quiz-core.test.cjs
```

Expected: FAIL because `quiz-core.js` does not exist.

- [ ] **Step 3: Implement the UMD core API**

Expose one immutable API in both environments:

```js
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  root.QuizCore = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  return Object.freeze({
    normalizeAnswer,
    gradeChoice,
    gradeFill,
    sampleWithoutReplacement,
    summarizeProgress,
    nextUnfinishedIndex,
    updateRecord,
    safeLoad,
    safeSave,
  });
});
```

Keep all functions pure except `safeLoad` and `safeSave`, which receive a storage object as an argument.

- [ ] **Step 4: Run tests and verify GREEN**

```powershell
node --test tests/quiz-core.test.cjs
```

Expected: all core tests PASS.

- [ ] **Step 5: Commit core slice**

```powershell
git add -- '大二下/计算机原理/刷题网站/quiz-core.js' '大二下/计算机原理/刷题网站/tests/quiz-core.test.cjs'
git commit -m "feat: add offline quiz grading and progress core"
```

### Task 4: Build the offline shell and responsive interface

**Files:**
- Create: `大二下/计算机原理/刷题网站/tests/static-site.test.mjs`
- Create: `大二下/计算机原理/刷题网站/index.html`
- Create: `大二下/计算机原理/刷题网站/styles.css`
- Create: `大二下/计算机原理/刷题网站/app.js`

- [ ] **Step 1: Write failing static contract tests**

Read `index.html` and assert it contains the viewport meta tag, skip link, status live region, `app-root`, local stylesheet, and classic scripts in this order: `questions.js`, `quiz-core.js`, `app.js`. Assert there are no `http://`, `https://`, CDN, module-script, or fetch dependencies.

- [ ] **Step 2: Run the static contract test and verify RED**

```powershell
node --test tests/static-site.test.mjs
```

Expected: FAIL because `index.html` does not exist.

- [ ] **Step 3: Implement semantic HTML and practical CSS**

Create a compact header, centered `main`, live feedback region, and root container. CSS must define visible focus states, 44 px minimum touch targets, semantic success/error colors plus text labels, a `72rem` shell, a `48rem` reading column, overflow-safe code and images, and a mobile sticky action bar.

- [ ] **Step 4: Implement screen rendering and events in `app.js`**

Use a single state object containing `screen`, `mode`, `chapter`, `queue`, `index`, `revealed`, and persisted records. Implement `renderHome`, `renderChapters`, `startChapter`, `startRandom`, `startMistakes`, `renderQuestion`, `submitObjective`, `revealShortAnswer`, `rateShortAnswer`, `goPrevious`, `goNext`, `renderSummary`, and `clearProgress`. Use event delegation on `app-root` and escape all text before injecting marked-up question content.

- [ ] **Step 5: Verify static tests and all unit tests**

```powershell
node --test tests/*.test.mjs tests/*.test.cjs
```

Expected: all tests PASS with no warnings.

- [ ] **Step 6: Commit interface slice**

```powershell
git add -- '大二下/计算机原理/刷题网站/index.html' '大二下/计算机原理/刷题网站/styles.css' '大二下/计算机原理/刷题网站/app.js' '大二下/计算机原理/刷题网站/tests/static-site.test.mjs'
git commit -m "feat: build offline computer principles quiz interface"
```

### Task 5: Document, package-check, and perform browser QA

**Files:**
- Create: `大二下/计算机原理/刷题网站/README.md`
- Modify after a reproduced QA failure only: the affected file among `index.html`, `styles.css`, `app.js`, or `quiz-core.js`, plus the regression test that fails before the fix

- [ ] **Step 1: Add a failing README contract**

Extend `static-site.test.mjs` to assert `README.md` explains: double-click opening, ZIP sharing, no installation, local-only progress, clearing progress, and the Node test command.

- [ ] **Step 2: Run and verify RED**

```powershell
node --test tests/static-site.test.mjs
```

Expected: FAIL because `README.md` does not exist.

- [ ] **Step 3: Write README and verify GREEN**

Write concise Chinese instructions and rerun all tests.

- [ ] **Step 4: Verify copied-folder offline behavior**

Copy the complete `刷题网站` directory into a temporary location, open its `index.html` by `file://`, and verify no network requests are required.

- [ ] **Step 5: Browser-test core flows at desktop and mobile sizes**

Verify: chapter entry; choice feedback; fill grading; short-answer reveal and self-rating; random no-repeat flow; mistakes removal; refresh restore; clear confirmation; retained diagrams; keyboard focus; mobile overflow.

- [ ] **Step 6: Run final automated verification**

```powershell
node scripts/build-questions.mjs
node --test tests/*.test.mjs tests/*.test.cjs
git diff --check
git status --short
```

Expected: the build succeeds, every test passes, no whitespace errors are reported, and the only unrelated worktree change remains the user's existing Chapter 6 Markdown edit.

- [ ] **Step 7: Commit documentation and QA fixes**

```powershell
git add -- '大二下/计算机原理/刷题网站'
git commit -m "docs: explain offline quiz use and sharing"
```
