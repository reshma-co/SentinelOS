from agents.base_agent import BaseAgent, AgentResult


class CommunicationAgent(BaseAgent):
    def run(self, task: str) -> AgentResult:
        message = f"""
🚨 FLOOD ALERT 🚨

Location: Kochi

Heavy rainfall has caused flooding.

Please evacuate immediately using the recommended safe route.

Nearest Shelter:
Community Hall, Kochi

Follow instructions from emergency authorities.
"""

        return AgentResult(
            name=self.name,
            output=message.strip()
        )


if __name__ == "__main__":
    agent = CommunicationAgent("communication-agent")
    result = agent.run("Generate flood alert")
    print(result.output)