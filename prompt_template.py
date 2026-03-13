"""Prompt templates for Hinglish conversion."""
from __future__ import annotations

TRANSLATION_PROMPT = """You are a translation engine.

TASK:
Convert the following English text into natural Hinglish (Hindi written in English letters).

STRICT RULES:

* Output ONLY Hinglish text.
* Do NOT add explanations.
* Do NOT add introductions.
* Do NOT add comments.
* Preserve formatting exactly.
* Preserve headings.
* Preserve paragraph structure.
* Preserve bullet lists.
* Preserve numbering.

Formatting markers like:
[HEADING]
[PARAGRAPH]
[LIST]

must remain unchanged.

Only translate the content text.

TEXT:
{chunk}
"""


def build_translation_prompt(chunk_text: str) -> str:
    """Return a fully rendered translation prompt for a chunk."""
    return TRANSLATION_PROMPT.format(chunk=chunk_text)
