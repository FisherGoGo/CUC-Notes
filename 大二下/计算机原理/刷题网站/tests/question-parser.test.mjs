import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import {
  parseChapter,
  rewriteAssetPaths,
  serializeQuestions,
  shouldExclude,
} from '../scripts/question-parser.mjs';

test('parses a choice question with answer and explanation', () => {
  const markdown = `# 第一章练习题

## 1. 总线

**题目：** 数据总线用于（ ）。

**选项：**

- A. 寻址
- B. 传数据

**答案：B**

**解析：** 数据总线传数据。`;

  const [question] = parseChapter(markdown, 1);

  assert.equal(question.id, 'ch01-q01');
  assert.equal(question.type, 'choice');
  assert.deepEqual(question.options, [
    { key: 'A', text: '寻址' },
    { key: 'B', text: '传数据' },
  ]);
  assert.equal(question.answer, 'B');
  assert.equal(question.explanation, '数据总线传数据。');
});

test('parses numbered blanks in order', () => {
  const markdown = `# 第十一章练习题

## 9. 总线分类

**题目：** ① 位于芯片内部，② 位于系统之间。

**答案：** ① 片内总线 ② 外总线

**解析：** 按范围分类。`;

  const [question] = parseChapter(markdown, 11);

  assert.equal(question.type, 'fill');
  assert.deepEqual(question.answer, ['片内总线', '外总线']);
  assert.deepEqual(question.acceptedAnswers, [['片内总线'], ['外总线']]);
});

test('cleans blank separators and expands common alternative answers', () => {
  const markdown = `# 第十一章练习题

## 11. AGP

**题目：** AGP 即 ①，属于 ②。

**答案：** ① 加速图形端口（或加速图形接口）；② 总线接口 / 图形接口
`;

  const [question] = parseChapter(markdown, 11);

  assert.deepEqual(question.answer, ['加速图形端口（或加速图形接口）', '总线接口 / 图形接口']);
  assert.deepEqual(question.acceptedAnswers, [
    ['加速图形端口', '加速图形接口'],
    ['总线接口', '图形接口'],
  ]);
});

test('classifies prose answers as short answer', () => {
  const markdown = `# 第六章练习题

## 21. 中断过程

**题目：** 简述中断处理过程。

**答案：** 请求、响应、保护现场、服务、恢复和返回。

**解析：** 按处理顺序作答。`;

  const [question] = parseChapter(markdown, 6);

  assert.equal(question.type, 'short');
  assert.match(question.answer, /保护现场/);
});

test('rewrites retained source images to local assets', () => {
  const markdown = '![图](../assets/9-12.png)';
  assert.equal(rewriteAssetPaths(markdown), '![图](assets/9-12.png)');
});

test('serializes questions as a classic browser script with CommonJS fallback', () => {
  const output = serializeQuestions([{ id: 'ch01-q01' }]);
  assert.match(output, /root\.QUIZ_QUESTIONS = questions/);
  assert.match(output, /module\.exports = questions/);
  assert.match(output, /"ch01-q01"/);
});

test('excludes the six programming questions and three image-dependent questions', () => {
  assert.equal(shouldExclude(4, 14), true);
  assert.equal(shouldExclude(7, 17), true);
  assert.equal(shouldExclude(7, 18), true);
  assert.equal(shouldExclude(7, 19), true);
  assert.equal(shouldExclude(9, 10), true);
  assert.equal(shouldExclude(9, 11), true);
  assert.equal(shouldExclude(5, 13), true);
  assert.equal(shouldExclude(5, 15), true);
  assert.equal(shouldExclude(9, 12), true);
});

test('parses and validates all eleven answered chapter banks', async () => {
  const testDirectory = path.dirname(fileURLToPath(import.meta.url));
  const homeworkDirectory = path.resolve(testDirectory, '../../HomeWork');
  const questions = [];

  for (let chapter = 1; chapter <= 11; chapter += 1) {
    const markdown = await readFile(
      path.join(homeworkDirectory, `第${chapter}章练习题.md`),
      'utf8',
    );
    questions.push(...parseChapter(markdown, chapter));
  }

  assert.equal(questions.length, 177);
  assert.deepEqual(
    [...new Set(questions.map((question) => question.chapter))],
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
  );
  assert.equal(
    questions.find((question) => question.chapter === 5).chapterTitle,
    '存储器',
  );
  assert.equal(new Set(questions.map((question) => question.id)).size, questions.length);

  const excludedIds = [
    'ch04-q14',
    'ch07-q17',
    'ch07-q18',
    'ch07-q19',
    'ch09-q10',
    'ch09-q11',
    'ch05-q13',
    'ch05-q15',
    'ch09-q12',
  ];
  for (const id of excludedIds) {
    assert.equal(questions.some((question) => question.id === id), false, id);
  }

  for (const question of questions) {
    assert.ok(question.prompt, `${question.id} must have a prompt`);
    assert.ok(
      Array.isArray(question.answer) ? question.answer.length : String(question.answer).trim(),
      `${question.id} must have an answer`,
    );

    if (question.type === 'choice') {
      assert.ok(question.options.length >= 2, `${question.id} must have options`);
      assert.ok(
        question.options.some((option) => option.key === question.answer),
        `${question.id} answer must match an option`,
      );
    }

    if (question.type === 'fill') {
      const blankCount = [...question.prompt].filter((character) => '①②③④⑤⑥⑦⑧⑨⑩'.includes(character)).length;
      assert.equal(question.answer.length, blankCount, `${question.id} blank count`);
    }

    assert.deepEqual(question.assets, [], `${question.id} must not require an image`);
  }

  const types = new Set(questions.map((question) => question.type));
  assert.deepEqual([...types].sort(), ['choice', 'fill', 'short']);
});
