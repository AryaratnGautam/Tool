# Document Reader

A production-ready static web application for turning uploaded documents into a beautiful reading interface while preserving the original text content. It runs entirely in the browser and is suitable for GitHub Pages.

## Features

- Client-side upload workflow for PDF, DOCX, TXT, Markdown, and optional HTML files.
- PDF.js text extraction for text-based PDFs; scanned PDFs are intentionally unsupported.
- Mammoth.js raw text extraction for DOCX files.
- Deterministic, non-AI parser that maps document structure into title, heading, subheading, paragraph, list, quote, table, code, and divider blocks.
- Dynamic navigation drawer generated from detected sections.
- Reading progress bar, active section highlighting, reading time estimate, dark mode, mobile layout, and back-to-top control.
- Static-only architecture: no backend, database, API calls, chatbot, analysis, summarization, or rewriting.

## Text integrity

The app is designed as a formatting and rendering tool. It does not rewrite, summarize, paraphrase, reorder, or intentionally alter document wording. Text is escaped before rendering to preserve visible characters safely in the browser.

Some source formats require unavoidable extraction behavior from browser libraries. For example, PDF text extraction may expose text in the order provided by the PDF text layer, and HTML files are read as source text instead of executing markup.

## Project structure

```text
/
├── index.html
├── css/
│   ├── styles.css
│   └── reader.css
├── js/
│   ├── app.js
│   ├── uploader.js
│   ├── parser.js
│   ├── renderer.js
│   ├── navigator.js
│   ├── theme.js
│   └── utils.js
└── libs/
```

PDF.js and Mammoth.js are loaded from CDN in `index.html` to keep the repository small and GitHub Pages friendly. If you require fully vendored dependencies, download the matching browser builds into `libs/` and update the script tags.

## Local setup

No build step is required. Serve the folder with any static server:

```bash
python3 -m http.server 8000
```

Open `http://localhost:8000` in your browser.

## GitHub Pages deployment

1. Push this repository to GitHub.
2. Open **Settings → Pages**.
3. Set **Source** to **Deploy from a branch**.
4. Select your branch and the repository root folder.
5. Save and wait for Pages to publish the static site.

## Usage

1. Open the deployed site.
2. Drag and drop a supported document, or click **Choose file**.
3. Read the formatted document in reader mode.
4. Use the drawer to jump between detected sections.
5. Toggle dark mode or start a new upload as needed.
