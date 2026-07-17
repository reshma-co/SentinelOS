from dataclasses import dataclass


@dataclass
class AgentResult:
    name: str
    output: str


class BaseAgent:
    def __init__(self, name: str) -> None:
        self.name = name

    def run(self, task: str) -> AgentResult:
        raise NotImplementedError("Agent subclasses must implement run().")
