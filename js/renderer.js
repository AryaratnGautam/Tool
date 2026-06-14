window.DocumentRenderer = (() => {
  const { escapeHtml, readingMinutes } = window.ReaderUtils;
  function render(parsed) {
    const root = document.getElementById('documentRoot');
    const fragment = document.createDocumentFragment();
    parsed.blocks.forEach(block => fragment.appendChild(renderBlock(block)));
    root.replaceChildren(fragment);
    document.getElementById('navTitle').textContent = parsed.title;
    document.getElementById('readingTime').textContent = `${readingMinutes(parsed.rawText)} min read`;
    document.getElementById('blockCount').textContent = `${parsed.blocks.length} blocks`;
    return parsed.blocks.filter(b => ['title','heading','subheading'].includes(b.type));
  }
  function renderBlock(block) {
    const wrap = document.createElement(block.type === 'divider' ? 'hr' : 'section');
    wrap.id = block.id || `block-${Math.random().toString(36).slice(2)}`;
    wrap.dataset.blockType = block.type;
    if (block.type === 'title') { wrap.className = 'doc-hero'; wrap.innerHTML = `<p class="section-label">Document title</p><h1 class="doc-title">${escapeHtml(block.text)}</h1>`; }
    else if (block.type === 'heading') { wrap.className = 'doc-section'; wrap.innerHTML = `<p class="section-label">Section</p><h2>${escapeHtml(block.text)}</h2>`; }
    else if (block.type === 'subheading') { wrap.className = 'doc-subheading'; wrap.innerHTML = `<h3>${escapeHtml(block.text)}</h3>`; }
    else if (block.type === 'paragraph') { wrap.className = 'doc-card'; wrap.innerHTML = `<p class="doc-paragraph">${escapeHtml(block.text)}</p>`; }
    else if (block.type === 'bulletList' || block.type === 'numberedList') { wrap.className = 'doc-list'; const tag = block.type === 'bulletList' ? 'ul' : 'ol'; wrap.innerHTML = `<${tag}>${block.items.map(item => `<li>${escapeHtml(item)}</li>`).join('')}</${tag}>`; }
    else if (block.type === 'quote') { wrap.className = 'doc-quote'; wrap.innerHTML = `<blockquote>${escapeHtml(block.text)}</blockquote>`; }
    else if (block.type === 'table') { wrap.className = 'doc-table'; wrap.innerHTML = `<table>${block.rows.map((row, i) => `<tr>${row.map(cell => `<${i === 0 ? 'th' : 'td'}>${escapeHtml(cell)}</${i === 0 ? 'th' : 'td'}>`).join('')}</tr>`).join('')}</table>`; }
    else if (block.type === 'code') { wrap.className = 'doc-code'; wrap.innerHTML = `<pre><code>${escapeHtml(block.text)}</code></pre>`; }
    else { wrap.className = 'doc-divider'; }
    return wrap;
  }
  return { render };
})();
