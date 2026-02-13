import re


class SecurityAgent:

    MAX_LENGTH = 5000  # evita custo inesperado com LLM

    @staticmethod
    def sanitize_text(text: str) -> str:
        if not isinstance(text, str):
            raise ValueError("Invalid input type")

        sanitized = re.sub(r"[<>;$`]", "", text)

        if len(sanitized.strip()) == 0:
            raise ValueError("Empty message after sanitization")

        if len(sanitized) > SecurityAgent.MAX_LENGTH:
            raise ValueError("Message too large")

        return sanitized.strip()

