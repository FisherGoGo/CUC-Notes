import test from 'node:test';
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const testDirectory = path.dirname(fileURLToPath(import.meta.url));
const outputPath = path.resolve(testDirectory, '../../计算机原理刷题.html');

test('builds one self-contained offline HTML file', async () => {
  const html = await readFile(outputPath, 'utf8');

  assert.match(html, /<meta name="viewport"/);
  assert.match(html, /id="app-root"/);
  assert.match(html, /id="live-status"/);
  assert.match(html, /const questions = \[/);
  assert.match(html, /root\.QuizCore = api/);
  assert.doesNotMatch(html, /data:image\//);
  assert.doesNotMatch(html, /<script[^>]+src=/i);
  assert.doesNotMatch(html, /<link[^>]+href=/i);
  assert.doesNotMatch(html, /https?:\/\//i);
});

test('contains practical chapter, random, mistake, and reset controls', async () => {
  const html = await readFile(outputPath, 'utf8');

  for (const copy of ['按章节练习', '全题库随机', '错题重练', '清空进度']) {
    assert.match(html, new RegExp(copy));
  }
});
