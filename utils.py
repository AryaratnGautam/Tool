"""Utility helpers for logging, filesystem, and retries."""
from __future__ import annotations

import json
import logging
import time
from pathlib import Path
from typing import Callable, TypeVar

T = TypeVar("T")


def setup_logging(level: int = logging.INFO) -> None:
    """Configure global logging format for the pipeline."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )


def ensure_dir(path: str | Path) -> Path:
    """Ensure a directory exists and return the Path object."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def retry_with_backoff(
    fn: Callable[[], T],
    retries: int = 3,
    base_delay: float = 1.0,
    backoff_factor: float = 2.0,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> T:
    """Retry an operation with exponential backoff."""
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            return fn()
        except exceptions as exc:  # pragma: no cover - generic helper
            last_error = exc
            if attempt == retries:
                break
            sleep_for = base_delay * (backoff_factor ** (attempt - 1))
            logging.warning("Attempt %s/%s failed: %s. Retrying in %.1fs", attempt, retries, exc, sleep_for)
            time.sleep(sleep_for)
    assert last_error is not None
    raise last_error


def load_json(path: str | Path) -> dict:
    """Load JSON file if present, otherwise return empty dict."""
    p = Path(path)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def save_json(path: str | Path, data: dict) -> None:
    """Save dict as pretty JSON."""
    p = Path(path)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
