from base_agent import AgentResult, BaseAgent


class StarterAgent(BaseAgent):
    def run(self, task: str) -> AgentResult:
        return AgentResult(
            name=self.name,
            output=f"Received task: {task}",
        )


if __name__ == "__main__":
    agent = StarterAgent("starter-agent")
    result = agent.run("Summarize the hackathon idea.")
    print(result)
