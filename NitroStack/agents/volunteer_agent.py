import json
from pathlib import Path

from agents.base_agent import BaseAgent, AgentResult


class VolunteerAgent(BaseAgent):
    def run(self, task: str) -> AgentResult:
        data_folder = Path(__file__).resolve().parent.parent / "data"

        with open(data_folder / "volunteers.json", "r") as file:
            volunteers = json.load(file)

        with open(data_folder / "shelters.json", "r") as file:
            shelters = json.load(file)

        available_volunteers = [
            volunteer
            for volunteer in volunteers
            if volunteer["available"]
        ]

        open_shelters = [
            shelter
            for shelter in shelters
            if shelter["status"] == "Open"
        ]

        output = {
            "task": task,
            "available_volunteers": available_volunteers,
            "available_shelters": open_shelters,
        }

        return AgentResult(
            name=self.name,
            output=json.dumps(output, indent=2),
        )


if __name__ == "__main__":
    agent = VolunteerAgent("volunteer-agent")
    result = agent.run("Flood response in Kochi")
    print(result.output)