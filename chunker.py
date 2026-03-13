"""Token-aware chunking for large structured documents."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Chunk:
    """Represents chunk text with order index."""

    index: int
    text: str
    approx_tokens: int


class TokenChunker:
    """Split text while preserving block boundaries and approximate token limits."""

    def __init__(self, min_tokens: int = 1500, max_tokens: int = 2000) -> None:
        self.min_tokens = min_tokens
        self.max_tokens = max_tokens

    @staticmethod
    def estimate_tokens(text: str) -> int:
        """Approximate tokens (good enough for chunk planning)."""
        return max(1, int(len(text.split()) * 1.3))

    def chunk_structured_text(self, structured_text: str) -> list[Chunk]:
        """Split on double-newline block boundaries into stable ordered chunks."""
        blocks = [b for b in structured_text.split("\n\n") if b.strip()]
        chunks: list[Chunk] = []

        cur_blocks: list[str] = []
        cur_tokens = 0

        for block in blocks:
            block_tokens = self.estimate_tokens(block)
            next_tokens = cur_tokens + block_tokens
            if cur_blocks and next_tokens > self.max_tokens:
                chunk_text = "\n\n".join(cur_blocks)
                chunks.append(Chunk(len(chunks), chunk_text, cur_tokens))
                cur_blocks = [block]
                cur_tokens = block_tokens
            else:
                cur_blocks.append(block)
                cur_tokens = next_tokens

        if cur_blocks:
            chunks.append(Chunk(len(chunks), "\n\n".join(cur_blocks), cur_tokens))

        return chunks
