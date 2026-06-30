import { readFile, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { parseChapter } from './question-parser.mjs';

const scriptDirectory = path.dirname(fileURLToPath(import.meta.url));
const siteDirectory = path.resolve(scriptDirectory, '..');
const courseDirectory = path.resolve(siteDirectory, '..');
const homeworkDirectory = path.join(courseDirectory, 'HomeWork');
const outputPath = path.join(courseDirectory, '计算机原理刷题.html');

const questions = [];
for (let chapter = 1; chapter <= 11; chapter += 1) {
  const markdown = await readFile(path.join(homeworkDirectory, `第${chapter}章练习题.md`), 'utf8');
  questions.push(...parseChapter(markdown, chapter));
}

if (questions.length !== 177) {
  throw new Error(`Expected 177 retained questions, received ${questions.length}.`);
}

const css = await readFile(path.join(siteDirectory, 'styles.css'), 'utf8');
const core = await readFile(path.join(siteDirectory, 'quiz-core.js'), 'utf8');
const app = await readFile(path.join(siteDirectory, 'app.js'), 'utf8');
const payload = JSON.stringify(questions).replaceAll('</script', '<\\/script');

const html = `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="color-scheme" content="light">
  <title>计算机原理刷题</title>
  <style>${css}</style>
</head>
<body>
  <a class="skip-link" href="#app-root">跳到主要内容</a>
  <header class="site-header">
    <div class="header-inner">
      <h1 class="brand">计算机原理刷题</h1>
      <span class="header-note">离线版 · 进度仅保存在本浏览器</span>
    </div>
  </header>
  <main id="app-root" class="page-shell" tabindex="-1">
    <p>正在加载题库……</p>
  </main>
  <div id="live-status" class="sr-only" aria-live="polite" aria-atomic="true"></div>
  <noscript><p class="page-shell">请启用浏览器 JavaScript 后使用刷题功能。</p></noscript>
  <script>(function (root) { 'use strict'; const questions = ${payload}; root.QUIZ_QUESTIONS = questions; })(globalThis);</script>
  <script>${core.replaceAll('</script', '<\\/script')}</script>
  <script>${app.replaceAll('</script', '<\\/script')}</script>
</body>
</html>
`;

await writeFile(outputPath, html, 'utf8');
console.log(`Built ${path.basename(outputPath)} with ${questions.length} questions (${Math.round(Buffer.byteLength(html) / 1024)} KiB).`);
