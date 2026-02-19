import re
from typing import Any

MAX_TEXT_LENGTH = 5000


def sanitize_text(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("Text must be string")

    text = text.strip()

    if len(text) == 0:
        raise ValueError("Empty text")

    if len(text) > MAX_TEXT_LENGTH:
        raise ValueError("Text exceeds allowed size")

    text = re.sub(r"[<>;$`]", "", text)

    return text


def sanitize_dict(data: dict[str, Any]) -> dict[str, Any]:
    clean = {}

    for k, v in data.items():
        if isinstance(v, str):
            clean[k] = sanitize_text(v)
        else:
            clean[k] = v

    return clean
