from decimal import Decimal, ROUND_HALF_UP


class MarginValidationAgent:

    @staticmethod
    def calculate_margin(valor_produto: Decimal, valor_comissao: Decimal) -> Decimal:
        if valor_produto <= 0:
            raise ValueError("Invalid product value")

        margem = (valor_comissao / valor_produto) * Decimal(100)
        return margem.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def validate(self, data: dict) -> dict:

        margem = self.calculate_margin(
            data["valor_produto"],
            data["valor_comissao"],
        )

        if data["valor_comissao"] > data["valor_produto"]:
            raise ValueError("Commission greater than product value")

        data["margem_percentual"] = margem
        return data
