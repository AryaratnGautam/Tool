"""CLI entrypoint for English-to-Hinglish conversion pipeline."""
from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path

from chunker import TokenChunker
from document_builder import DocumentBuilder
from llm_client import OpenRouterClient, validate_markers
from ocr_engine import OCREngine
from pdf_processor import PDFProcessor
from text_cleaner import TextCleaner
from utils import ensure_dir, setup_logging

logger = logging.getLogger(__name__)


def process_pdf_input(pdf_path: Path, temp_dir: Path) -> str:
    """Extract text + OCR text from PDF."""
    processor = PDFProcessor(temp_dir=temp_dir)
    ocr = OCREngine()
    page_contents = processor.process(pdf_path)

    final_parts: list[str] = []
    for page in page_contents:
        page_text = page.text
        if page.image_paths:
            ocr_text = ocr.extract_text(page.image_paths)
            if ocr_text:
                page_text = f"{page_text}\n{ocr_text}".strip()
        if page_text:
            final_parts.append(page_text)

    return "\n\n".join(final_parts).strip()


def translate_text_to_hinglish(raw_text: str, api_key: str, stream: bool = False) -> str:
    """Run normalization, structuring, chunk translation, and merge outputs."""
    cleaner = TextCleaner()
    chunker = TokenChunker(min_tokens=1500, max_tokens=2000)
    client = OpenRouterClient(api_key=api_key)

    normalized = cleaner.normalize(raw_text)
    blocks = cleaner.structure(normalized)
    structured = cleaner.serialize(blocks)

    chunks = chunker.chunk_structured_text(structured)
    logger.info("Created %s chunk(s) for translation", len(chunks))

    translated_chunks: list[str] = []
    for chunk in chunks:
        logger.info("Translating chunk %s (%s tokens approx)", chunk.index + 1, chunk.approx_tokens)
        translated = client.translate_chunk(chunk.text, stream=stream)
        if not validate_markers(translated):
            raise ValueError(f"Marker validation failed for chunk {chunk.index}")
        translated_chunks.append(translated)

    return "\n\n".join(translated_chunks)


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(description="Convert English PDF/text into Hinglish while preserving formatting.")
    parser.add_argument("--pdf", type=Path, help="Path to input PDF")
    parser.add_argument("--text", type=str, help="Raw pasted English text")
    parser.add_argument("--api-key", type=str, default=os.getenv("OPENROUTER_API_KEY"), help="OpenRouter API key")
    parser.add_argument("--output-docx", type=Path, default=Path("output/output_hinglish.docx"), help="Output DOCX path")
    parser.add_argument("--output-pdf", type=Path, default=None, help="Optional output PDF path")
    parser.add_argument("--stream", action="store_true", help="Use streaming API responses if supported")
    return parser.parse_args()


def main() -> None:
    """Execute end-to-end conversion workflow."""
    setup_logging()
    args = parse_args()

    if not args.api_key:
        raise SystemExit("OpenRouter API key required. Set --api-key or OPENROUTER_API_KEY.")

    if not args.pdf and not args.text:
        raise SystemExit("Provide either --pdf or --text input.")

    temp_dir = ensure_dir(".processing/images")

    if args.pdf:
        logger.info("Input mode: PDF")
        raw_text = process_pdf_input(args.pdf, temp_dir)
    else:
        logger.info("Input mode: Raw text")
        raw_text = args.text.strip()

    if not raw_text:
        raise SystemExit("No text extracted from input.")

    translated_structured = translate_text_to_hinglish(raw_text, args.api_key, stream=args.stream)

    builder = DocumentBuilder()
    builder.build_docx(translated_structured, args.output_docx)
    if args.output_pdf:
        builder.build_pdf_optional(translated_structured, args.output_pdf)

    logger.info("Pipeline completed successfully.")


if __name__ == "__main__":
    main()
