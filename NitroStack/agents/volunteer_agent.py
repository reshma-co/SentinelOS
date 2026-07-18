import json
from pathlib import Path

from agents.base_agent import BaseAgent, AgentResult

DEFAULT_VOLUNTEERS = [
    {"name": "Asha Relief Team", "available": True, "skills": ["shelter", "first aid"], "count": 18},
    {"name": "Youth Response Cell", "available": True, "skills": ["logistics", "crowd support"], "count": 20},
    {"name": "Community Kitchen Unit", "available": True, "skills": ["food", "supplies"], "count": 12},
    {"name": "Night Patrol Volunteers", "available": False, "skills": ["field checks"], "count": 8},
]

DEFAULT_SHELTERS = [
    {"name": "ABC School", "status": "Open", "capacity": 600, "location": "Kochi, Kerala"},
    {"name": "Community Hall", "status": "Open", "capacity": 350, "location": "Kochi, Kerala"},
    {"name": "Town Sports Complex", "status": "Standby", "capacity": 800, "location": "Kochi, Kerala"},
]


def _load_json_or_default(path: Path, default: list[dict]) -> list[dict]:
    if not path.exists():
        return default
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


class VolunteerAgent(BaseAgent):
    def run(self, task: str) -> AgentResult:
        data_folder = Path(__file__).resolve().parent.parent / "data"

        volunteers = _load_json_or_default(data_folder / "volunteers.json", DEFAULT_VOLUNTEERS)
        shelters = _load_json_or_default(data_folder / "shelters.json", DEFAULT_SHELTERS)

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
            "total_available_volunteers": sum(item.get("count", 1) for item in available_volunteers),
            "total_shelter_capacity": sum(item.get("capacity", 0) for item in open_shelters),
        }

        return AgentResult(
            name=self.name,
            output=json.dumps(output, indent=2),
        )


if __name__ == "__main__":
    agent = VolunteerAgent("volunteer-agent")
    result = agent.run("Flood response in Kochi")
    print(result.output)
