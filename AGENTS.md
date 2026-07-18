# AI Agent Operating Instructions for SentinelOS

This file defines the operating rules for AI coding assistants such as Codex, Claude, and other development agents working on SentinelOS.

The purpose of this file is to prevent duplicate workspaces, accidental overwrites, architectural drift, and conflicts between team members.

---

## 1. Before Starting Any Implementation

Before making any code changes:

1. Read `PROJECT_CONTEXT.md`.
2. Run `git status`.
3. Confirm the active Git branch.
4. Inspect the relevant existing code before editing.
5. Check whether another teammate has already implemented related functionality.
6. Treat `PROJECT_CONTEXT.md` as project context, but treat the actual working code as authoritative for implementation details.
7. If `PROJECT_CONTEXT.md` conflicts with the current code, investigate the discrepancy instead of blindly following either one.

Do not begin implementation until the current repository state is understood.

---

## 2. Canonical Repository

The canonical Git repository is:

`C:\Users\sreek\OneDrive\Desktop\NEXA - nitrostack hackathon`

The main SentinelOS/NitroStack application is located inside:

`C:\Users\sreek\OneDrive\Desktop\NEXA - nitrostack hackathon\NitroStack`

The outer directory is the Git repository root.

The nested `NitroStack` directory is the application root containing:

- backend
- agents
- MCP servers
- tests
- frontend
- data
- documentation
- scripts

Do not create or maintain a second independent SentinelOS or NitroStack workspace.

Temporary ZIP extraction folders or AI-generated development folders must not become independent project copies.

All final implementation work must be integrated into the canonical Git repository.

---

## 3. Preserve Team Work

SentinelOS is developed by multiple team members.

Never overwrite teammate work without first inspecting and integrating it.

When modifying shared files such as:

`NitroStack/backend/app/main.py`

do not replace the entire file with a version from another branch, ZIP file, or generated workspace.

Instead:

1. Inspect the current canonical file.
2. Inspect the incoming implementation.
3. Merge imports additively.
4. Merge routes additively.
5. Preserve existing teammate endpoints and functionality.
6. Run tests after integration.

Current examples of functionality that must be preserved include:

- Health endpoint
- Volunteer Agent endpoint
- Communication Agent endpoint
- Mission Commander endpoints

When merging Git branches, inspect the resulting shared files before proceeding.

---

## 4. Critical SentinelOS Architecture Rules

### RULE 1 - No Default Incident

Never hardcode Flood as the default incident.

Flood may be used as a test or demonstration scenario only.

All real mission input must come from runtime user or tool input.

---

### RULE 2 - Scenario Agnostic Mission Commander

Mission Commander must remain scenario-agnostic.

Do not implement:

`incident type -> fixed emergency workflow`

Use:

`runtime incident -> analysis -> required capabilities -> available organization capabilities/tools -> coordinated response`

---

### RULE 3 - Capability-Based Coordination

Mission Commander coordinates capabilities.

Organization selection should be based on required capabilities.

Do not activate every organization for every incident.

---

### RULE 4 - Organization Logic Stays Outside Mission Commander

Organization-specific operational logic belongs inside organization modules or agents.

Mission Commander is responsible for:

- mission creation
- incident analysis
- capability determination
- organization selection
- dispatch
- response collection
- prioritization
- coordination
- unified mission planning
- mission status

Mission Commander should not contain detailed organization-specific response procedures.

---

### RULE 5 - Unknown Incidents Must Be Safe

Unknown or ambiguous incidents must remain classified as unknown when appropriate.

Never silently convert an unknown incident into Flood or another known scenario.

---

### RULE 6 - Do Not Fabricate External Results

Never claim that live APIs, MCP servers, sensors, databases, or external systems were used unless the implementation actually uses them.

Clearly distinguish between:

- real MCP tools
- local Python agents
- deterministic logic
- mocked organization responses
- live external integrations

---

### RULE 7 - Preserve Existing NitroStack Patterns

Reuse existing:

- FastAPI patterns
- Pydantic models
- MCP SDK conventions
- installed package versions
- repository structure

Do not invent unsupported MCP decorators, framework APIs, or integration patterns.

---

### RULE 8 - Canonical Repository Is Source of Truth

The canonical GitHub repository is the single source of truth.

Do not maintain a second independent implementation.

Code generated in temporary folders must be reviewed and migrated into the canonical repository before being considered part of SentinelOS.

---

## 5. Shared FastAPI Rules

The primary FastAPI application is:

`NitroStack/backend/app/main.py`

When integrating new functionality:

- preserve `/`
- preserve `/health`
- preserve `/volunteer`
- preserve `/communication`
- preserve Mission Commander routes
- add new routes without deleting teammate routes

Current Mission Commander routes include:

- `POST /mission`
- `POST /mission/{mission_id}/analyze`
- `GET /mission/{mission_id}/status`
- `POST /mission/run`

The primary demo endpoint is:

`POST /mission/run`

Do not change API contracts without checking tests and dependent modules.

---

## 6. Mission Commander Rules

Mission Commander implementation is located under:

`NitroStack/backend/app/mission/`

Before modifying Mission Commander:

1. Inspect schemas.
2. Inspect mission service.
3. Inspect capability registry.
4. Inspect organization implementations.
5. Inspect commander orchestration.
6. Inspect storage.
7. Inspect Mission Commander tests.

Mission Commander must continue to support multiple incident types.

Flood-specific behavior must never become the default behavior.

---

## 7. MCP Rules

MCP-related code is located under:

`NitroStack/mcp/`

Use only MCP APIs and decorators supported by the installed MCP Python SDK.

Do not assume that a local Python agent is automatically an MCP tool.

Documentation must clearly distinguish:

- MCP-exposed functionality
- FastAPI endpoints
- local Python agents
- mocked organization responses

When implementing new MCP functionality, expose existing tested application logic where possible instead of duplicating business logic.

---

## 8. Testing Rules

After every meaningful implementation:

1. Run relevant targeted tests.
2. Run the complete test suite when integration affects shared functionality.
3. Confirm that existing functionality still works.
4. Record verified results in `PROJECT_CONTEXT.md`.

Preferred full test command from the application root:

`backend\.venv\Scripts\python.exe -m pytest -v`

Do not claim functionality is working only because the code exists.

Working status requires verification through tests, API execution, or another appropriate runtime check.

Warnings must be documented separately from failures.

The current known Starlette/FastAPI TestClient deprecation warning does not represent a failed test.

---

## 9. Documentation Rules

After every meaningful implementation:

1. Update `PROJECT_CONTEXT.md`.
2. Update Current State.
3. Update Testing Status if tests changed.
4. Update Development Log.
5. Update Next Recommended Step.

Only add entries to Decision Log when an actual architectural or product decision is made.

Documentation must reflect verified implementation status.

Do not describe planned functionality as implemented.

Do not describe mocked functionality as live integration.

Never store:

- passwords
- API keys
- access tokens
- authentication secrets

in `PROJECT_CONTEXT.md`, `AGENTS.md`, or committed source files.

---

## 10. Git Workflow

Before editing:

`git status`

After implementation:

1. Run tests.
2. Inspect `git status`.
3. Review modified and untracked files.
4. Stage only intended files.
5. Commit with a descriptive message.
6. Push to the correct branch.

Before merging another teammate's branch:

1. Commit or safely preserve current work.
2. Fetch remote branches.
3. Inspect the incoming changes.
4. Merge.
5. Resolve shared-file conflicts carefully.
6. Run the complete test suite.

Never force-push or rewrite teammate history unless explicitly authorized.

---

## 11. Architectural Conflict Rule

Before changing architecture in a way that conflicts with a Critical Architectural Rule in `PROJECT_CONTEXT.md`:

STOP.

Explain:

- the proposed change
- the conflicting architectural rule
- why the change may be necessary
- the impact on existing modules

Do not silently override recorded architecture decisions.

---

## 12. Definition of Done

A development task is considered complete only when applicable:

- implementation exists in the canonical repository
- teammate functionality is preserved
- relevant tests pass
- full integration tests pass when required
- API behavior is verified when required
- documentation reflects the new state
- Git status has been reviewed
- changes are committed to the intended branch

The goal is not merely to generate code.

The goal is to maintain one coherent, tested, scenario-agnostic SentinelOS system.