const CIRCLED_NUMBERS = '①②③④⑤⑥⑦⑧⑨⑩';

const EXCLUDED_QUESTIONS = new Set([
  '4-14',
  '7-17',
  '7-18',
  '7-19',
  '9-10',
  '9-11',
]);

const BLOCK_MARKERS = [
  '题目',
  '选项',
  '答案',
  '解析',
  '干扰项分析',
];

export function shouldExclude(chapter, sourceNumber) {
  return EXCLUDED_QUESTIONS.has(`${Number(chapter)}-${Number(sourceNumber)}`);
}

export function rewriteAssetPaths(markdown) {
  return String(markdown ?? '').replaceAll('../assets/', 'assets/');
}

function cleanBlock(value) {
  return rewriteAssetPaths(String(value ?? ''))
    .replace(/^\s+|\s+$/g, '')
    .replace(/\r\n/g, '\n');
}

function markerPattern(label) {
  return new RegExp(`\\*\\*${label}：\\*\\*`, 'g');
}

function findNextBoundary(section, fromIndex, currentLabel) {
  const positions = [];
  for (const label of BLOCK_MARKERS) {
    if (label === currentLabel) continue;
    const pattern = markerPattern(label);
    pattern.lastIndex = fromIndex;
    const match = pattern.exec(section);
    if (match) positions.push(match.index);
  }

  const answerInline = /\*\*答案：(?!\*\*)/g;
  answerInline.lastIndex = fromIndex;
  const inlineMatch = answerInline.exec(section);
  if (currentLabel !== '答案' && inlineMatch) positions.push(inlineMatch.index);

  const pitfall = /^>\s*易错点：/gm;
  pitfall.lastIndex = fromIndex;
  const pitfallMatch = pitfall.exec(section);
  if (pitfallMatch) positions.push(pitfallMatch.index);

  const subheading = /^###\s+/gm;
  subheading.lastIndex = fromIndex;
  const subheadingMatch = subheading.exec(section);
  if (subheadingMatch) positions.push(subheadingMatch.index);

  return positions.length ? Math.min(...positions) : section.length;
}

function extractBlock(section, label) {
  const pattern = markerPattern(label);
  const match = pattern.exec(section);
  if (!match) return '';
  const start = match.index + match[0].length;
  const end = findNextBoundary(section, start, label);
  return cleanBlock(section.slice(start, end));
}

function extractAnswer(section) {
  const inline = /\*\*答案：([\s\S]*?)\*\*/.exec(section);
  if (!inline) return '';
  const inside = cleanBlock(inline[1]);
  if (inside) return inside;

  const start = inline.index + inline[0].length;
  const end = findNextBoundary(section, start, '答案');
  return cleanBlock(section.slice(start, end));
}

function extractOptions(section) {
  const optionsBlock = extractBlock(section, '选项');
  const options = [];
  const optionPattern = /^-\s+([A-Z])\.\s+(.+?)(?=\n-\s+[A-Z]\.\s+|$)/gms;
  for (const match of optionsBlock.matchAll(optionPattern)) {
    options.push({
      key: match[1],
      text: cleanBlock(match[2]),
    });
  }
  return options;
}

function normalizeInlineAnswer(value) {
  return cleanBlock(value)
    .replace(/^\*\*|\*\*$/g, '')
    .replace(/\n+/g, ' ')
    .trim();
}

export function extractNumberedAnswers(answerText) {
  const text = cleanBlock(answerText);
  const markerClass = `[${CIRCLED_NUMBERS}]`;
  const pattern = new RegExp(`${markerClass}\\s*([\\s\\S]*?)(?=${markerClass}|$)`, 'g');
  return [...text.matchAll(pattern)]
    .map((match) => normalizeInlineAnswer(match[1]))
    .filter(Boolean);
}

function extractPitfall(section) {
  const match = /^>\s*易错点：\s*(.+)$/m.exec(section);
  return match ? cleanBlock(match[1]) : '';
}

function extractAssets(...blocks) {
  const assets = [];
  const pattern = /!\[[^\]]*\]\((assets\/[^)]+)\)/g;
  for (const block of blocks) {
    for (const match of String(block).matchAll(pattern)) {
      if (!assets.includes(match[1])) assets.push(match[1]);
    }
  }
  return assets;
}

export function parseQuestionSection(section, chapterNumber, sourceNumber, title) {
  const prompt = extractBlock(section, '题目');
  const options = extractOptions(section);
  const rawAnswer = extractAnswer(section);
  const explanation = extractBlock(section, '解析');
  const distractorAnalysis = extractBlock(section, '干扰项分析');
  const pitfall = extractPitfall(section);
  const blankMarkers = [...prompt].filter((character) => CIRCLED_NUMBERS.includes(character));

  let type = 'short';
  let answer = rawAnswer;
  let acceptedAnswers = [];

  if (options.length) {
    type = 'choice';
    answer = rawAnswer.replace(/[^A-Z]/g, '').slice(0, 1);
  } else if (blankMarkers.length) {
    type = 'fill';
    answer = extractNumberedAnswers(rawAnswer);
    acceptedAnswers = answer.map((item) => [item]);
  }

  const paddedChapter = String(chapterNumber).padStart(2, '0');
  const paddedQuestion = String(sourceNumber).padStart(2, '0');

  return {
    id: `ch${paddedChapter}-q${paddedQuestion}`,
    chapter: Number(chapterNumber),
    chapterTitle: `第${chapterNumber}章`,
    sourceNumber: Number(sourceNumber),
    type,
    title: cleanBlock(title),
    prompt,
    options,
    answer,
    acceptedAnswers,
    explanation,
    distractorAnalysis,
    pitfall,
    assets: extractAssets(prompt, explanation),
  };
}

export function parseChapter(markdown, chapterNumber) {
  const text = String(markdown ?? '').replace(/\r\n/g, '\n');
  const headings = [...text.matchAll(/^##\s+(\d+)\.\s+(.+)$/gm)];
  const questions = [];

  headings.forEach((heading, index) => {
    const sourceNumber = Number(heading[1]);
    if (shouldExclude(chapterNumber, sourceNumber)) return;
    const start = heading.index + heading[0].length;
    const end = headings[index + 1]?.index ?? text.length;
    const section = text.slice(start, end);
    questions.push(parseQuestionSection(section, chapterNumber, sourceNumber, heading[2]));
  });

  return questions;
}
