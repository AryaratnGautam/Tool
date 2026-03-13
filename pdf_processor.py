"""PDF text extraction orchestration using PyMuPDF."""
from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

import fitz

from image_extractor import extract_images_from_page

logger = logging.getLogger(__name__)


@dataclass
class PDFPageContent:
    """Container for per-page extracted data."""

    page_number: int
    text: str
    image_paths: list[Path]


class PDFProcessor:
    """Extract selectable text and images from PDF pages."""

    def __init__(self, temp_dir: Path) -> None:
        self.temp_dir = temp_dir

    def process(self, pdf_path: str | Path) -> list[PDFPageContent]:
        """Return per-page text and extracted images for OCR."""
        pages: list[PDFPageContent] = []
        pdf_path = Path(pdf_path)
        logger.info("Opening PDF: %s", pdf_path)
        with fitz.open(pdf_path) as doc:
            for page_idx in range(len(doc)):
                page = doc[page_idx]
                text = page.get_text("text") or ""
                images = extract_images_from_page(doc, page_idx, self.temp_dir)
                pages.append(PDFPageContent(page_idx + 1, text.strip(), images))
                logger.info(
                    "Processed page %s/%s | text_chars=%s | images=%s",
                    page_idx + 1,
                    len(doc),
                    len(text),
                    len(images),
                )
        return pages
