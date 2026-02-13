from app.agents.security import SecurityAgent
from app.agents.extractor import ExtractorAgent
from app.agents.validator import ValidatorAgent
from app.agents.margin import MarginValidationAgent
from app.agents.description import DescriptionAgent
from app.agents.crm import CRMClassifierAgent


class MessageProcessingCrew:

    def __init__(self):
        self.security = SecurityAgent()
        self.extractor = ExtractorAgent()
        self.validator = ValidatorAgent()
        self.margin = MarginValidationAgent()
        self.description = DescriptionAgent()
        self.crm = CRMClassifierAgent()

    def process(self, raw_text: str) -> dict:

        text = self.security.sanitize_text(raw_text)

        data = self.extractor.extract(text)

        data = self.validator.validate(data)

        data = self.margin.validate(data)

        data["descricao_melhorada"] = self.description.improve(
            data["descricao_original"]
        )

        data["classificacao"] = self.crm.classify(
            data["margem_percentual"]
        )

        return data
