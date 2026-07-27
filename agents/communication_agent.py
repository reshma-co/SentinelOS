from agents.base_agent import BaseAgent, AgentResult


class CommunicationAgent(BaseAgent):
    def run(self, task: str) -> AgentResult:
        task_text = task.strip() or "Emergency response"
        message = f"""
EMERGENCY ALERT

Task: {task_text}

Follow Mission Commander instructions from local authorities.
Move away from the affected zone if evacuation is advised.

Nearest Shelter:
Community Hall, Kochi

Updates will be broadcast through official emergency channels.
"""

        return AgentResult(
            name=self.name,
            output=message.strip(),
        )


if __name__ == "__main__":
    agent = CommunicationAgent("communication-agent")
    result = agent.run("Generate emergency alert")
    print(result.output)
