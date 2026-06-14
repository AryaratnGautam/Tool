window.DocumentUploader = (() => {
  const { fileExtension } = window.ReaderUtils;
  async function extract(file) {
    const ext = fileExtension(file);
    if (ext === 'pdf' || file.type === 'application/pdf') return extractPdf(file);
    if (ext === 'docx') return extractDocx(file);
    if (['txt','md','markdown','html','htm'].includes(ext) || file.type.startsWith('text/')) return file.text();
    throw new Error('Unsupported file type. Please upload PDF, DOCX, TXT, Markdown, or HTML.');
  }
  async function extractPdf(file) {
    if (!window.pdfjsLib) throw new Error('PDF.js failed to load. Check your network connection.');
    pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
    const pdf = await pdfjsLib.getDocument({ data: await file.arrayBuffer() }).promise;
    const pages = [];
    for (let pageNumber = 1; pageNumber <= pdf.numPages; pageNumber++) {
      const page = await pdf.getPage(pageNumber); const content = await page.getTextContent();
      pages.push(content.items.map(item => item.str).join(' '));
      if (pageNumber % 20 === 0) await new Promise(requestAnimationFrame);
    }
    return pages.join('\n\n');
  }
  async function extractDocx(file) {
    if (!window.mammoth) throw new Error('Mammoth.js failed to load. Check your network connection.');
    const result = await mammoth.extractRawText({ arrayBuffer: await file.arrayBuffer() });
    return result.value;
  }
  function init(onParsed) {
    const input = document.getElementById('fileInput'); const choose = document.getElementById('chooseFile'); const dropzone = document.getElementById('dropzone'); const status = document.getElementById('status');
    choose.addEventListener('click', () => input.click()); input.addEventListener('change', () => input.files[0] && handle(input.files[0]));
    ['dragenter','dragover'].forEach(type => dropzone.addEventListener(type, event => { event.preventDefault(); dropzone.classList.add('dragover'); }));
    ['dragleave','drop'].forEach(type => dropzone.addEventListener(type, event => { event.preventDefault(); dropzone.classList.remove('dragover'); }));
    dropzone.addEventListener('drop', event => event.dataTransfer.files[0] && handle(event.dataTransfer.files[0]));
    async function handle(file) {
      try { status.textContent = `Reading ${file.name}…`; const raw = await extract(file); const parsed = DocumentParser.parseText(raw, { fileName: file.name, markdown: ['md','markdown'].includes(fileExtension(file)) }); onParsed(parsed); status.textContent = ''; }
      catch (error) { console.error(error); status.textContent = error.message; }
    }
  }
  return { init, extract };
})();
