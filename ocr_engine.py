"""OCR abstraction using PaddleOCR with Tesseract fallback."""
from __future__ import annotations

import logging
from pathlib import Path

from PIL import Image

logger = logging.getLogger(__name__)

try:
    from paddleocr import PaddleOCR
except Exception:  # pragma: no cover
    PaddleOCR = None

try:
    import pytesseract
except Exception:  # pragma: no cover
    pytesseract = None


class OCREngine:
    """Runs OCR over extracted images and returns ordered text."""

    def __init__(self, use_angle_cls: bool = True, lang: str = "en") -> None:
        self.ocr = None
        self.backend = None

        if PaddleOCR is not None:
            self.ocr = PaddleOCR(use_angle_cls=use_angle_cls, lang=lang)
            self.backend = "paddleocr"
            logger.info("OCR backend: PaddleOCR")
        elif pytesseract is not None:
            self.backend = "tesseract"
            logger.info("OCR backend: Tesseract")
        else:
            raise RuntimeError("No OCR backend available. Install paddleocr or pytesseract.")

    def extract_text(self, image_paths: list[Path]) -> str:
        """Extract OCR text from images and merge in reading order."""
        lines: list[str] = []
        for image_path in image_paths:
            if self.backend == "paddleocr":
                result = self.ocr.ocr(str(image_path), cls=True)  # type: ignore[union-attr]
                for block in result:
                    if not block:
                        continue
                    sorted_block = sorted(block, key=lambda item: (item[0][0][1], item[0][0][0]))
                    for entry in sorted_block:
                        text = entry[1][0].strip()
                        if text:
                            lines.append(text)
            else:
                text = pytesseract.image_to_string(Image.open(image_path))
                for line in text.splitlines():
                    stripped = line.strip()
                    if stripped:
                        lines.append(stripped)

        return "\n".join(lines).strip()
