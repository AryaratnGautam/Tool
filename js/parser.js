window.DocumentParser = (() => {
  const { slugify, words } = window.ReaderUtils;

  function parseText(raw, options = {}) {
    const normalized = String(raw || '').replace(/\r\n?/g, '\n');
    const lines = normalized.split('\n');
    const blocks = [];
    let i = 0;
    let headingCount = 0;
    const push = block => blocks.push({ id: `block-${blocks.length}`, ...block });

    while (i < lines.length) {
      const line = lines[i];
      const trimmed = line.trim();
      if (!trimmed) { push({ type: 'paragraph', text: line }); i++; continue; }
      if (/^(```|~~~)/.test(trimmed)) {
        const fence = trimmed.slice(0, 3); const code = [line]; i++;
        while (i < lines.length) { code.push(lines[i]); if (lines[i].trim().startsWith(fence)) { i++; break; } i++; }
        push({ type: 'code', text: code.join('\n') }); continue;
      }
      if (/^(-{3,}|_{3,}|\*{3,})$/.test(trimmed)) { push({ type: 'divider', text: line }); i++; continue; }
      if (isTableStart(lines, i)) { const table = []; while (i < lines.length && lines[i].includes('|')) table.push(lines[i++]); push({ type: 'table', rows: parseTable(table), text: table.join('\n') }); continue; }
      if (/^\s*([-*•])\s+/.test(line)) { const items = []; while (i < lines.length && /^\s*([-*•])\s+/.test(lines[i])) items.push(lines[i++].replace(/^\s*([-*•])\s+/, '')); push({ type: 'bulletList', items, text: items.join('\n') }); continue; }
      if (/^\s*\d+[.)]\s+/.test(line)) { const items = []; while (i < lines.length && /^\s*\d+[.)]\s+/.test(lines[i])) items.push(lines[i++].replace(/^\s*\d+[.)]\s+/, '')); push({ type: 'numberedList', items, text: items.join('\n') }); continue; }
      if (/^\s*>\s?/.test(line) || /^\s*[«“].*[»”]\s*$/.test(trimmed)) { const quotes = []; while (i < lines.length && (/^\s*>\s?/.test(lines[i]) || (quotes.length === 0 && /^\s*[«“]/.test(lines[i].trim())))) quotes.push(lines[i++].replace(/^\s*>\s?/, '')); push({ type: 'quote', text: quotes.join('\n') }); continue; }
      const heading = classifyHeading(line, blocks.length, options.markdown);
      if (heading) { const id = slugify(heading.text, ++headingCount); push({ ...heading, id }); i++; continue; }
      const para = [line]; i++;
      while (i < lines.length && lines[i].trim() && !isBoundary(lines, i, options.markdown)) para.push(lines[i++]);
      push({ type: 'paragraph', text: para.join('\n') });
    }
    if (!blocks.some(b => b.type === 'title')) {
      const firstText = blocks.find(b => b.text && b.text.trim());
      if (firstText) { firstText.type = 'title'; firstText.id = slugify(firstText.text, 0); }
    }
    return { blocks, rawText: normalized, title: deriveTitle(blocks, options.fileName) };
  }

  function classifyHeading(line, index, markdown) {
    const trimmed = line.trim();
    const md = trimmed.match(/^(#{1,6})\s+(.+)$/);
    if (markdown && md) return { type: md[1].length === 1 && index < 3 ? 'title' : md[1].length <= 2 ? 'heading' : 'subheading', text: md[2] };
    if (index < 3 && trimmed.length < 140 && (/^[A-Z0-9\s:;,.&'’!?-]+$/.test(trimmed) || words(trimmed) <= 14)) return { type: 'title', text: line };
    if (/^(chapter|part|section)\s+\w+/i.test(trimmed) || /^\d+(\.\d+)*[.)]?\s+\S+/.test(trimmed)) return { type: 'heading', text: line };
    if (trimmed.length < 90 && !/[.!?]$/.test(trimmed) && words(trimmed) <= 10) return { type: 'subheading', text: line };
    return null;
  }
  const isBoundary = (lines, i, markdown) => !lines[i].trim() || classifyHeading(lines[i], 99, markdown) || /^\s*([-*•]|\d+[.)]|>|```|~~~)/.test(lines[i]) || isTableStart(lines, i);
  const isTableStart = (lines, i) => lines[i]?.includes('|') && lines[i + 1]?.match(/^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$/);
  const parseTable = rows => rows.filter((_, i) => i !== 1).map(row => row.replace(/^\||\|$/g, '').split('|').map(cell => cell.trim()));
  const deriveTitle = (blocks, fileName) => (blocks.find(b => b.type === 'title' && b.text?.trim())?.text || fileName || 'Untitled document').trim();
  return { parseText };
})();
