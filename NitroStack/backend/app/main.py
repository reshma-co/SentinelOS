from fastapi import FastAPI
from pydantic import BaseModel

from agents.volunteer_agent import VolunteerAgent
from agents.communication_agent import CommunicationAgent


class HealthResponse(BaseModel):
    status: str
    service: str


app = FastAPI(
    title="NitroStack API",
    version="0.1.0"
)


@app.get("/")
def read_root():
    return {"message": "NitroStack backend is running"}


@app.get("/health", response_model=HealthResponse)
def health_check():
    return HealthResponse(
        status="ok",
        service="nitrostack-backend"
    )


@app.get("/volunteer")
def volunteer():
    agent = VolunteerAgent("volunteer-agent")
    result = agent.run("Flood response in Kochi")
    return {
        "agent": result.name,
        "output": result.output
    }


@app.get("/communication")
def communication():
    agent = CommunicationAgent("communication-agent")
    result = agent.run("Generate flood alert")
    return {
        "agent": result.name,
        "output": result.output
    }