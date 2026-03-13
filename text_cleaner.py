"""Normalize text and map to structural tags for format preservation."""
from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass
class StructuredBlock:
    """Represents a formatting-aware content block."""

    kind: str
    text: str


class TextCleaner:
    """Normalize whitespace while preserving paragraphs, headings, and lists."""

    heading_re = re.compile(r"^(?:[A-Z][A-Z\s\-\d]{3,}|#+\s+.+)$")
    list_re = re.compile(r"^(?:[-*•]\s+|\d+[.)]\s+).+")

    def normalize(self, text: str) -> str:
        """Normalize text without breaking intentional line/paragraph boundaries."""
        normalized_lines: list[str] = []
        for line in text.splitlines():
            line = re.sub(r"[ \t]+", " ", line).rstrip()
            normalized_lines.append(line)

        # Keep blank lines to preserve paragraph breaks.
        return "\n".join(normalized_lines).strip()

    def structure(self, text: str) -> list[StructuredBlock]:
        """Convert plain text to tagged block representation."""
        blocks: list[StructuredBlock] = []
        for para in self._paragraphs(text):
            if self.heading_re.match(para):
                blocks.append(StructuredBlock("HEADING", para))
            elif self.list_re.match(para):
                blocks.append(StructuredBlock("LIST", para))
            else:
                blocks.append(StructuredBlock("PARAGRAPH", para))
        return blocks

    def serialize(self, blocks: list[StructuredBlock]) -> str:
        """Serialize structured blocks into marker-based format for LLM translation."""
        return "\n\n".join(f"[{block.kind}]\n{block.text}" for block in blocks)

    @staticmethod
    def _paragraphs(text: str) -> list[str]:
        paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
        return paras
