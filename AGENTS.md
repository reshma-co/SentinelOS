# Codex Operating Instructions For SentinelOS

Before starting any implementation task in this repository:

1. Read `PROJECT_CONTEXT.md`.
2. Inspect the relevant existing code before editing.
3. Treat `PROJECT_CONTEXT.md` as project context, but treat actual working code as authoritative for implementation details.
4. If `PROJECT_CONTEXT.md` conflicts with the current code, investigate the discrepancy instead of blindly following either one.
5. Do not create a new duplicate SentinelOS/NitroStack workspace.
6. Work only inside the canonical repository unless explicitly instructed otherwise.
7. Never hardcode Flood as the default incident.
8. Keep Mission Commander scenario-agnostic.
9. Preserve teammate work.
10. After every meaningful implementation:
    - run relevant tests
    - update `PROJECT_CONTEXT.md`
    - update Current State
    - update Development Log
    - update Next Recommended Step
11. Add to Decision Log only when an actual architectural or product decision is made.
12. Never store passwords, API keys, tokens, or secrets in `PROJECT_CONTEXT.md`.
13. Before changing architecture in a way that conflicts with a recorded Critical Architectural Rule, stop and explain the conflict.

Repository rules:

- The canonical GitHub repository is `C:\Users\sreek\OneDrive\Desktop\NEXA - nitrostack hackathon`.
- The nested `NitroStack` directory contains the current application scaffold.
- Do not maintain a second independent project workspace.
- Reuse existing NitroStack patterns and installed package versions.
- Do not invent unsupported MCP decorators, APIs, or framework patterns.
- Organization-specific logic belongs inside organization modules, not Mission Commander.
- Mission Commander coordinates capabilities and structured outputs.
