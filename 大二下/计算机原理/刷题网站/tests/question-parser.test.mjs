import test from 'node:test';
import assert from 'node:assert/strict';

import {
  parseChapter,
  rewriteAssetPaths,
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

test('excludes only the six approved programming questions', () => {
  assert.equal(shouldExclude(4, 14), true);
  assert.equal(shouldExclude(7, 17), true);
  assert.equal(shouldExclude(7, 18), true);
  assert.equal(shouldExclude(7, 19), true);
  assert.equal(shouldExclude(9, 10), true);
  assert.equal(shouldExclude(9, 11), true);
  assert.equal(shouldExclude(9, 12), false);
});
