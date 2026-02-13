import re
import os
from decimal import Decimal
from typing import Optional
from app.core.config import settings


class ExtractorAgent:

    PRODUCT_REGEX = re.compile(
        r"(?P<nome>.+?)\n.*?(?P<descricao>.+?)\n.*?R?\$?\s?(?P<valor>\d+[.,]?\d*)\n.*?R?\$?\s?(?P<comissao>\d+[.,]?\d*)",
        re.DOTALL,
    )

    @staticmethod
    def _parse_decimal(value: str) -> Decimal:
        normalized = value.replace(",", ".")
        return Decimal(normalized)

    def extract(self, text: str) -> dict:

        match = self.PRODUCT_REGEX.search(text)

        if match:
            return {
                "nome": match.group("nome").strip(),
                "descricao_original": match.group("descricao").strip(),
                "valor_produto": self._parse_decimal(match.group("valor")),
                "valor_comissao": self._parse_decimal(match.group("comissao")),
            }

        # Fallback LLM (opcional)
        if settings.OPENAI_API_KEY:
            return self._llm_fallback(text)

        raise ValueError("Regex extraction failed and no LLM fallback configured")

    def _llm_fallback(self, text: str) -> dict:
        from crewai import Agent, Task, Crew, Process

        extractor = Agent(
            role="Structured Data Extractor",
            goal="Extract product info as JSON",
            backstory="You extract structured data from messy WhatsApp messages.",
            verbose=False,
        )

        task = Task(
            description=(
                "Extract nome, descricao_original, valor_produto, valor_comissao "
                "from the following text and return JSON only:\n\n"
                f"{text}"
            ),
            expected_output="JSON with fields nome, descricao_original, valor_produto, valor_comissao",
            agent=extractor,
        )

        crew = Crew(
            agents=[extractor],
            tasks=[task],
            process=Process.sequential,
        )

        result = crew.kickoff().strip()

import json

try:
    data = json.loads(result)
except json.JSONDecodeError:
    raise ValueError("LLM returned invalid JSON")

return {
    "nome": data["nome"],
    "descricao_original": data["descricao_original"],
    "valor_produto": Decimal(str(data["valor_produto"])),
    "valor_comissao": Decimal(str(data["valor_comissao"])),
}

