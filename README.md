Here is a ready-to-paste `README.md` formatted specifically for your repo architecture.

---

```markdown
# 🛡️ SentinelOS — Crisis Coordination System

**SentinelOS** is an autonomous, multi-agent disaster response command system built using the **Model Context Protocol (MCP)**. It dynamically orchestrates specialized operational nodes (Weather, Transport, Hospital, Police, Volunteer, and Communication) to evaluate real-time hazards, prioritize life-saving actions, and generate unified mission plans during emergency situations.

---

## 🔥 Key Features

* **Scenario-Agnostic Mission Commander:** Evaluates incident descriptions dynamically at runtime without hardcoded defaults.
* **Autonomous Multi-Agent Mesh:** Dispatches only the required capabilities (Weather, Hospital, Police, Transport, Volunteers, EAS) based on incident classification.
* **Domain-Aware Risk Evaluation:** Dynamic hazard assessment tailored specifically to the emergency type (e.g., Seismic & Aftershock analysis for Earthquakes, Containment/Evacuation protocols for Chemical Leaks).
* **Live Command Dashboard:** Built-in Leaflet JS interactive map synced directly with the backend's mission context, showing active operations areas, priority action timelines, and agency status.
* **Exportable Incident Reports:** One-click JSON report generation containing full mission timelines, allocated resources, and evacuation routes.

---

## 🏗️ System Architecture

```text
SentinelOS/
├── backend/
│   └── app/
│       ├── api/               # FastAPI endpoints (/mission/start, /health)
│       ├── mcp/               # Clean MCP service tier
│       │   ├── services.py    # Core domain logic & tool integration
│       │   └── data.py        # Simulated emergency resources/hospitals/roads
│       ├── mission/           # Mission Commander orchestration engine
│       │   ├── commander.py   # Parallel dispatching & priority aggregation
│       │   ├── schemas.py     # Pydantic data schemas
│       │   └── storage.py     # In-memory mission state storage
│       └── main.py            # FastAPI application entry point
└── frontend/
    ├── index.html             # Real-time command center interface
    ├── styles.css             # Cyberpunk/Tech UI dashboard styling
    └── js/
        ├── api.js             # Backend API client integration
        ├── main.js            # Workflow orchestrator & state manager
        ├── map.js             # Leaflet JS map controller & coordinate lookup
        └── ui.js              # Dynamic DOM renderer

```

---

## 🚀 Quick Start Guide

### Prerequisites

* Python 3.10+
* Node.js / Modern Browser

### 1. Start Backend Server

```bash
# From project root
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run Uvicorn
uvicorn app.main:app --reload --port 8000

```

* Backend API live at: `http://127.0.0.1:8000`
* Swagger Documentation: `http://127.0.0.1:8000/docs`

### 2. Launch Dashboard Frontend

```bash
# Open a new terminal from project root
cd frontend
python -m http.server 3000

```

* Open `http://localhost:3000` in your web browser.

---

## 🛣️ Future Roadmap

* **Multi-City Region Selector:** Enable operators to explicitly select target operational zones (e.g., Kochi, Mumbai, Bengaluru) directly from the command dashboard.
* **Opt-In Emergency Geolocation:** Integrate optional browser-based geolocation (`navigator.geolocation`) to automatically center disaster response operations on an emergency reporter's exact location during critical events while preserving privacy controls.

```

```
