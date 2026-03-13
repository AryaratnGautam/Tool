"""Image extraction utilities for PDF pages."""
from __future__ import annotations

import logging
from pathlib import Path

import fitz

logger = logging.getLogger(__name__)


def extract_images_from_page(doc: fitz.Document, page_index: int, out_dir: Path) -> list[Path]:
    """Extract images from a single PDF page and return saved file paths."""
    page = doc[page_index]
    images = page.get_images(full=True)
    saved: list[Path] = []

    for i, image_meta in enumerate(images, start=1):
        xref = image_meta[0]
        img_dict = doc.extract_image(xref)
        ext = img_dict.get("ext", "png")
        image_bytes = img_dict["image"]
        output_file = out_dir / f"page_{page_index + 1}_img_{i}.{ext}"
        output_file.write_bytes(image_bytes)
        saved.append(output_file)
        logger.debug("Saved image %s", output_file)

    return saved
