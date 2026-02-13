from decimal import Decimal


class CRMClassifierAgent:

    def classify(self, margem_percentual: Decimal) -> str:

        if margem_percentual >= Decimal("10"):
            return "quente"
        elif margem_percentual >= Decimal("5"):
            return "morno"
        else:
            return "frio"

