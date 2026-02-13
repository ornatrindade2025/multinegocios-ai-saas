from app.agents.crew import MessageProcessingCrew


class CrewService:

    def __init__(self):
        self.crew = MessageProcessingCrew()

    def process_message(self, raw_text: str) -> dict:
        return self.crew.process(raw_text)
