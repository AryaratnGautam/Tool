"""OpenRouter client with retries, caching, and optional streaming."""
from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path

import requests

from prompt_template import build_translation_prompt
from utils import load_json, retry_with_backoff, save_json

logger = logging.getLogger(__name__)


class OpenRouterClient:
    """Client wrapper for chunk-by-chunk translation using OpenRouter."""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-opus-120b",
        cache_file: str | Path = ".cache/chunk_cache.json",
        timeout_s: int = 90,
    ) -> None:
        self.api_key = api_key
        self.model = model
        self.timeout_s = timeout_s
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"
        self.cache_file = Path(cache_file)
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        self.cache = load_json(self.cache_file)

    def translate_chunk(self, chunk_text: str, stream: bool = False) -> str:
        """Translate a structured chunk into Hinglish with caching and retries."""
        key = hashlib.sha256(chunk_text.encode("utf-8")).hexdigest()
        if key in self.cache:
            logger.info("Cache hit for chunk=%s", key[:8])
            return self.cache[key]

        prompt = build_translation_prompt(chunk_text)

        def _call_api() -> str:
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": stream,
                "temperature": 0.1,
            }
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            }
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=self.timeout_s)
            response.raise_for_status()

            if stream:
                return self._collect_streamed_response(response)

            data = response.json()
            return data["choices"][0]["message"]["content"].strip()

        translated = retry_with_backoff(_call_api, retries=4, base_delay=1.5)
        self.cache[key] = translated
        save_json(self.cache_file, self.cache)
        return translated

    @staticmethod
    def _collect_streamed_response(response: requests.Response) -> str:
        """Collect streamed chunks from OpenRouter SSE response."""
        chunks: list[str] = []
        for line in response.iter_lines(decode_unicode=True):
            if not line or not line.startswith("data:"):
                continue
            payload = line.replace("data:", "", 1).strip()
            if payload == "[DONE]":
                break
            try:
                content = json.loads(payload)["choices"][0]["delta"].get("content", "")
                if content:
                    chunks.append(content)
            except Exception:
                continue
        return "".join(chunks).strip()


def validate_markers(text: str) -> bool:
    """Ensure at least one marker exists in response; simple guard for malformed output."""
    markers = ("[HEADING]", "[PARAGRAPH]", "[LIST]")
    return any(marker in text for marker in markers)
