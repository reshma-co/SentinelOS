# SentinelOS Project Context

## 1. Project Identity

Project Name: SentinelOS

Team: NEXA

Purpose:
SentinelOS is an AI-powered multi-organization emergency coordination platform built using MCP and NitroStack.

Core principle:
The system is NOT a scenario-specific chatbot.

It is a generic emergency coordination protocol where a Mission Commander dynamically analyzes incidents and coordinates relevant organizational capabilities through MCP.

The system must NEVER default to flood or any other incident.

Flood is only one possible test/demo scenario.

Canonical repository:
`C:\Users\sreek\OneDrive\Desktop\NEXA - nitrostack hackathon`

Duplicate/development workspace identified during audit:
`C:\Users\sreek\OneDrive\Documents\New project\NitroStack`

## 2. Core Architecture

Intended architecture:

```text
User Runtime Input
        |
        v
Mission Commander
        |
        v
Create Mission
        |
        v
Analyze Incident
        |
        v
Determine Required Capabilities
        |
        v
Capability Router
        |
        v
Select Relevant Organizational MCP Tools
        |
        v
Execute Tools
        |
        v
Collect Structured Responses
        |
        v
Coordinate / Prioritize
        |
        v
Generate Unified Mission Plan
        |
        v
Mission Dashboard + Incident Report
```

Mission Commander is scenario-agnostic. It should classify and analyze runtime incident input, derive required capabilities, route those capabilities to available organizational MCP modules, collect structured responses, and generate a unified mission plan. It must not encode a fixed incident type to fixed workflow mapping.

## 3. Mission Commander Protocol

Phase 1 - create and analyze mission:
- `create_mission`
- `analyze_incident`
- Status: IN PROGRESS. Implemented in duplicate workspace only, not yet migrated into the canonical GitHub repository.

Phase 2 - capability routing:
- capability registry
- `dispatch_agents`
- Status: PLANNED - NOT IMPLEMENTED.

Phase 3 - coordination execution:
- `execute_coordination`
- organization tool integration
- Status: PLANNED - NOT IMPLEMENTED.

Phase 4 - mission plan:
- `generate_mission_plan`
- Status: PLANNED - NOT IMPLEMENTED.

Phase 5 - status and reports:
- `get_mission_status`
- `generate_incident_report`
- Status: PLANNED - NOT IMPLEMENTED.

Phase 6 - UI integration:
- Mission Dashboard
- widgets
- Status: PLANNED - NOT IMPLEMENTED.

## 4. MCP Modules

### Existing In Canonical Repository

#### Sample MCP Server

Purpose:
Minimal MCP server scaffold.

Current implementation status:
IMPLEMENTED as starter scaffold in `NitroStack/mcp/sample_server.py`.

MCP tools:
- `echo`

MCP resources:
- `nitrostack://status`

MCP prompts:
- None found.

Services:
- None found.

External APIs:
- None found.

Dependencies:
- Python MCP SDK from `NitroStack/backend/requirements.txt`.

Owner/team member:
- Not documented in repository text files.

Known limitations:
- Starter server only. It does not include Mission Commander tools in the canonical repository yet.

### Existing Only In Duplicate Workspace

#### MissionModule

Purpose:
Mission Commander Phase 1: create mission records from runtime input and analyze incidents into mission context.

Current implementation status:
IN PROGRESS in duplicate workspace only at `C:\Users\sreek\OneDrive\Documents\New project\NitroStack\mcp\mission`. Requires migration confirmation before being copied into the canonical repository.

MCP tools:
- `create_mission`
- `analyze_incident`

MCP resources:
- None found.

MCP prompts:
- None found.

Services:
- `MissionService`
- `IncidentAnalysisService`

External APIs:
- None. The analysis implementation is deterministic keyword-based logic.

Dependencies:
- `mcp`
- `pydantic`
- `pytest` for duplicate workspace tests.

Owner/team member:
- Not documented in repository text files.

Known limitations:
- In-memory mission storage for the lifetime of the MCP server process.
- Deterministic classifier only; no live external data or organization tool dispatch.
- Exists in duplicate workspace, not canonical repo.

### Intended Modules

#### WeatherModule

Purpose:
Provide weather and environmental risk capabilities.

Current implementation status:
PLANNED - NOT IMPLEMENTED.

MCP tools:
PLANNED - NOT IMPLEMENTED.

MCP resources:
PLANNED - NOT IMPLEMENTED.

MCP prompts:
PLANNED - NOT IMPLEMENTED.

Services:
PLANNED - NOT IMPLEMENTED.

External APIs:
PLANNED - NOT IMPLEMENTED.

Dependencies:
PLANNED - NOT IMPLEMENTED.

Owner/team member:
Not documented.

Known limitations:
PLANNED - NOT IMPLEMENTED.

#### HospitalModule

Purpose:
Provide emergency medical response and ambulance support capabilities.

Current implementation status:
PLANNED - NOT IMPLEMENTED.

MCP tools:
PLANNED - NOT IMPLEMENTED.

MCP resources:
PLANNED - NOT IMPLEMENTED.

MCP prompts:
PLANNED - NOT IMPLEMENTED.

Services:
PLANNED - NOT IMPLEMENTED.

External APIs:
PLANNED - NOT IMPLEMENTED.

Dependencies:
PLANNED - NOT IMPLEMENTED.

Owner/team member:
Not documented.

Known limitations:
PLANNED - NOT IMPLEMENTED.

#### PoliceModule

Purpose:
Provide traffic control, perimeter security, and public safety capabilities.

Current implementation status:
PLANNED - NOT IMPLEMENTED.

MCP tools:
PLANNED - NOT IMPLEMENTED.

MCP resources:
PLANNED - NOT IMPLEMENTED.

MCP prompts:
PLANNED - NOT IMPLEMENTED.

Services:
PLANNED - NOT IMPLEMENTED.

External APIs:
PLANNED - NOT IMPLEMENTED.

Dependencies:
PLANNED - NOT IMPLEMENTED.

Owner/team member:
Not documented.

Known limitations:
PLANNED - NOT IMPLEMENTED.

#### TransportModule

Purpose:
Provide road status, route planning, rescue transport, and logistics capabilities.

Current implementation status:
PLANNED - NOT IMPLEMENTED.

MCP tools:
PLANNED - NOT IMPLEMENTED.

MCP resources:
PLANNED - NOT IMPLEMENTED.

MCP prompts:
PLANNED - NOT IMPLEMENTED.

Services:
PLANNED - NOT IMPLEMENTED.

External APIs:
PLANNED - NOT IMPLEMENTED.

Dependencies:
PLANNED - NOT IMPLEMENTED.

Owner/team member:
Not documented.

Known limitations:
PLANNED - NOT IMPLEMENTED.

#### VolunteerModule

Purpose:
Provide manpower, shelter support, relief distribution, and field volunteer capabilities.

Current implementation status:
PLANNED - NOT IMPLEMENTED.

MCP tools:
PLANNED - NOT IMPLEMENTED.

MCP resources:
PLANNED - NOT IMPLEMENTED.

MCP prompts:
PLANNED - NOT IMPLEMENTED.

Services:
PLANNED - NOT IMPLEMENTED.

External APIs:
PLANNED - NOT IMPLEMENTED.

Dependencies:
PLANNED - NOT IMPLEMENTED.

Owner/team member:
Not documented.

Known limitations:
PLANNED - NOT IMPLEMENTED.

#### CommunicationModule

Purpose:
Provide public alert and emergency broadcast capabilities.

Current implementation status:
PLANNED - NOT IMPLEMENTED.

MCP tools:
PLANNED - NOT IMPLEMENTED.

MCP resources:
PLANNED - NOT IMPLEMENTED.

MCP prompts:
PLANNED - NOT IMPLEMENTED.

Services:
PLANNED - NOT IMPLEMENTED.

External APIs:
PLANNED - NOT IMPLEMENTED.

Dependencies:
PLANNED - NOT IMPLEMENTED.

Owner/team member:
Not documented.

Known limitations:
PLANNED - NOT IMPLEMENTED.

## 5. Mission Input Contract

Canonical runtime input:

```json
{
  "incident_description": "string",
  "location": "string",
  "severity": "string optional",
  "timestamp": "string optional"
}
```

Rules:
- `incident_description` is required.
- `location` is required.
- There is no default incident.
- There is no default flood.
- Incident classification occurs at runtime.

Duplicate workspace implementation:
- `CreateMissionInput` requires non-empty `incident_description` and `location`.
- Optional `severity` and `timestamp` are trimmed; empty strings become `None`.

## 6. Mission Context Contract

Canonical repository current status:
Mission context schema is not yet implemented in the canonical repository.

Duplicate workspace actual schema:

```json
{
  "mission_id": "string",
  "incident_type": "string",
  "location": "string",
  "severity": "low | medium | high | critical | unknown",
  "hazards": ["string"],
  "required_capabilities": ["string"],
  "status": "analyzed"
}
```

Additional duplicate workspace mission record schema:

```json
{
  "mission_id": "string",
  "incident_description": "string",
  "location": "string",
  "reported_severity": "string optional",
  "timestamp": "string",
  "status": "created"
}
```

Implementation difference from the conceptual contract:
- The duplicate implementation stores the original input in a separate `Mission` model and returns analyzed operational fields in `MissionContext`.
- The canonical repository has not yet migrated these models.

## 7. Capability Registry

Current capabilities from duplicate Mission Commander implementation:
- `weather_conditions`
- `environmental_risk`
- `emergency_medical_response`
- `ambulance_support`
- `evacuation`
- `traffic_control`
- `perimeter_security`
- `road_status`
- `route_planning`
- `rescue_transport`
- `logistics`
- `shelter_support`
- `relief_distribution`
- `manpower`
- `public_alert`
- `emergency_broadcast`

Planned capability to module mapping:
- `weather_conditions` -> WeatherModule
- `environmental_risk` -> WeatherModule
- `emergency_medical_response` -> HospitalModule
- `ambulance_support` -> HospitalModule
- `evacuation` -> PoliceModule, TransportModule, VolunteerModule
- `traffic_control` -> PoliceModule
- `perimeter_security` -> PoliceModule
- `road_status` -> TransportModule
- `route_planning` -> TransportModule
- `rescue_transport` -> TransportModule
- `logistics` -> TransportModule, VolunteerModule
- `shelter_support` -> VolunteerModule
- `relief_distribution` -> VolunteerModule
- `manpower` -> VolunteerModule
- `public_alert` -> CommunicationModule
- `emergency_broadcast` -> CommunicationModule

Architecture rule:
Use `incident -> required capabilities -> available MCP tools`.

Do not encode `incident type -> fixed scenario workflow`.

## 8. Critical Architectural Rules

RULE 1:
Never hardcode Flood as the default incident.

RULE 2:
Never use example scenarios as production defaults.

RULE 3:
All mission input must come from runtime user/tool input.

RULE 4:
Mission Commander must remain scenario-agnostic.

RULE 5:
Organization-specific logic belongs inside organization modules, not Mission Commander.

RULE 6:
Mission Commander coordinates capabilities and structured outputs.

RULE 7:
Do not activate every organization for every incident.

RULE 8:
Unknown incidents must be handled safely and must not default to a known scenario.

RULE 9:
Do not fabricate external API or MCP tool results.

RULE 10:
Do not break or overwrite teammate modules when implementing new features.

RULE 11:
Reuse existing NitroStack patterns and installed package versions. Do not invent unsupported decorators or APIs.

RULE 12:
The canonical GitHub repository is the single source of truth. Do not create a second independent project workspace.

## 9. Repository Structure

Current important canonical repository structure:

```text
C:\Users\sreek\OneDrive\Desktop\NEXA - nitrostack hackathon
|-- .gitignore
|-- AGENTS.md
|-- PROJECT_CONTEXT.md
|-- nitrodesp.pdf
`-- NitroStack
    |-- .env.example
    |-- README.md
    |-- agents
    |   |-- base_agent.py
    |   `-- starter_agent.py
    |-- backend
    |   |-- requirements.txt
    |   `-- app
    |       `-- main.py
    |-- data
    |   `-- .gitkeep
    |-- docs
    |   `-- setup-notes.md
    |-- frontend
    |-- mcp
    |   |-- sample_client.py
    |   `-- sample_server.py
    |-- scripts
    |   `-- check_backend.ps1
    `-- tests
        `-- test_health.py
```

Major directories:
- `NitroStack/backend`: FastAPI backend scaffold and backend Python requirements.
- `NitroStack/mcp`: MCP sample server and client scaffold.
- `NitroStack/agents`: starter agent abstractions.
- `NitroStack/tests`: pytest test files.
- `NitroStack/scripts`: local verification scripts.
- `NitroStack/docs`: setup notes and project documentation.
- `NitroStack/data`: placeholder for local ignored data.
- `NitroStack/frontend`: empty frontend placeholder.

## 10. Technology Stack

Technologies verified in the repository:
- Git
- GitHub remote: `https://github.com/reshma-co/NEXA-NitroStack.git`
- Python
- FastAPI
- Pydantic
- MCP Python SDK
- Uvicorn
- Requests
- python-dotenv
- pytest test style, though `pytest` is not currently installed in the canonical repo venv

NitroStack is present as the project scaffold/directory name and README identity.

## 11. External Integrations

Currently integrated:
- None verified beyond local FastAPI and MCP sample code.

Currently mocked/stubbed:
- MCP sample `echo` tool.
- MCP sample `nitrostack://status` resource.
- Starter agent returns a local string response.

Planned or placeholder environment variables in `NitroStack/.env.example`:
- `APP_NAME`
- `ENVIRONMENT`
- `API_HOST`
- `API_PORT`
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GITHUB_TOKEN`

Integration status:
- `OPENAI_API_KEY`: planned/placeholder, no verified code integration.
- `ANTHROPIC_API_KEY`: planned/placeholder, no verified code integration.
- `GITHUB_TOKEN`: planned/placeholder, no verified code integration.

Never store secret values in this file.

## 12. Testing Status

Canonical repository test command:

```powershell
cd "C:\Users\sreek\OneDrive\Desktop\NEXA - nitrostack hackathon\NitroStack"
python -m pytest
```

Latest canonical repository result on 2026-07-18:
- Not run successfully with system Python: `No module named pytest`.
- Not run successfully with `NitroStack/backend/.venv/Scripts/python.exe`: `No module named pytest`.
- Canonical repository currently contains one health test: `NitroStack/tests/test_health.py`.

Duplicate workspace test command:

```powershell
cd "C:\Users\sreek\OneDrive\Documents\New project\NitroStack"
backend\.venv\Scripts\python.exe -m pytest
```

Latest duplicate workspace result on 2026-07-18:
- 9 tests passed.
- 1 warning: Starlette/httpx deprecation warning from FastAPI TestClient.

MCP verification status:
- Direct MCP-compatible verification has not been run in the canonical repository.
- Directly running an MCP stdio server in a terminal may produce JSON-RPC parsing errors if it receives invalid stdin. Proper MCP verification should use an MCP-compatible client such as the repository's sample client or another MCP client.

## 13. Decision Log

### 2026-07-18 - Scenario-Agnostic Mission Commander

Decision:
SentinelOS uses a scenario-agnostic Mission Commander.

Reason:
The platform must coordinate emergency capabilities for many incident types, not behave as a scenario-specific chatbot.

Impact:
Mission Commander should analyze runtime input and derive capabilities dynamically.

### 2026-07-18 - Flood Is A Test Scenario

Decision:
Flood is a test/demo scenario, not the default protocol.

Reason:
Defaulting to flood would make the platform brittle and violate the generic emergency coordination goal.

Impact:
All mission creation and incident analysis must come from runtime input.

### 2026-07-18 - Capability-Based Routing

Decision:
Capability-based routing is preferred over fixed scenario routing.

Reason:
Organizations should be selected based on required capabilities and available MCP tools.

Impact:
Mission Commander should map incidents to capabilities, then route to organization modules.

### 2026-07-18 - Canonical Repository Is Source Of Truth

Decision:
`C:\Users\sreek\OneDrive\Desktop\NEXA - nitrostack hackathon` is the canonical GitHub repository and single source of truth.

Reason:
It is a Git repository with remote `https://github.com/reshma-co/NEXA-NitroStack.git`, branch `reshma`, and existing team history. The Documents-side `NitroStack` folder is a separate no-commit Git repo with no remote.

Impact:
Future work should happen only inside the canonical repository unless explicitly instructed. Do not maintain two independent SentinelOS/NitroStack workspaces.

## 14. Development Log

### 2026-07-18

Completed:
- Audited the canonical GitHub repository and duplicate development workspace.
- Created persistent project context in the canonical repository.
- Created Codex operating instructions in the canonical repository.

Changed:
- Added `PROJECT_CONTEXT.md`.
- Added `AGENTS.md`.
- No application code was moved or migrated.

Tested:
- Duplicate workspace tests: 9 passed using its backend venv.
- Canonical repository tests could not run because `pytest` is not installed in the canonical venv or system Python.

Next:
- Review and confirm the minimal Mission Commander migration plan before copying implementation files into the canonical repository.

## 15. Current State

What currently works:
- Canonical FastAPI health endpoint scaffold exists.
- Canonical MCP sample server exposes `echo` and `nitrostack://status`.
- Duplicate workspace Mission Commander Phase 1 works in tests.

What is partially implemented:
- Mission Commander Phase 1 is implemented only in the duplicate workspace.
- Canonical repository has starter backend/MCP/agent scaffolding but not Mission Commander.

What is mocked:
- MCP sample `echo` tool.
- MCP sample status resource.
- Starter agent response.

What is broken:
- Canonical repository test execution is blocked because `pytest` is not installed in the canonical environment.
- Project organization was split across the canonical GitHub repository and a duplicate no-remote workspace.

What has been tested:
- Duplicate workspace: 9 pytest tests passed.
- Canonical repository: pytest was attempted but missing.

What should be built next:
- Migrate the minimum Mission Commander Phase 1 files from the duplicate workspace into the canonical repository after confirmation, then install/align test dependencies and run tests.

## 16. Next Recommended Step

Confirm the minimal Mission Commander Phase 1 migration into the canonical GitHub repository.
