from decimal import Decimal, ROUND_HALF_UP


class ValidatorAgent:

    @staticmethod
    def normalize_decimal(value: Decimal) -> Decimal:
        return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    def validate(self, data: dict) -> dict:

        required_fields = [
            "nome",
            "descricao_original",
            "valor_produto",
            "valor_comissao",
        ]

        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing field: {field}")

        data["valor_produto"] = self.normalize_decimal(data["valor_produto"])
        data["valor_comissao"] = self.normalize_decimal(data["valor_comissao"])

        return data
