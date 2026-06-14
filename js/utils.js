window.ReaderUtils = (() => {
  const escapeHtml = (value = '') => String(value).replace(/[&<>'"]/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));
  const slugify = (text, index) => `section-${index}-${String(text).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '').slice(0, 48) || 'untitled'}`;
  const words = text => (String(text).match(/\S+/g) || []).length;
  const readingMinutes = text => Math.max(1, Math.ceil(words(text) / 225));
  const fileExtension = file => (file.name.split('.').pop() || '').toLowerCase();
  return { escapeHtml, slugify, words, readingMinutes, fileExtension };
})();
