from app.core.config import settings


class DescriptionAgent:

    def improve(self, descricao: str) -> str:

        if not settings.OPENAI_API_KEY:
            return descricao  # Sem LLM

        from crewai import Agent, Task, Crew, Process

        agent = Agent(
            role="Sales Copywriter",
            goal="Improve product description for conversion",
            backstory="You specialize in persuasive product descriptions.",
            verbose=False,
        )

        task = Task(
            description=f"Rewrite this description to improve sales conversion:\n\n{descricao}",
            expected_output="Improved persuasive description text",
            agent=agent,
        )

        crew = Crew(
            agents=[agent],
            tasks=[task],
            process=Process.sequential,
        )

        return crew.kickoff()
