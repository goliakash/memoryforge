# 🧠 AI Security Operations & Compliance Memory Agent
### *Persistent Organizational Memory for SecOps and Compliance Powered by Hindsight*

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-19-cyan.svg)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite-6.0-purple.svg)](https://vitejs.dev)
[![Tests Passing](https://img.shields.io/badge/Tests-11%20Passed-brightgreen.svg)]()

---

## 🏗️ Repository Architecture

This project is organized into two primary workstreams: **Backend** (FastAPI AI Core & Hindsight Memory Engine) and **Frontend** (React + Vite Web Dashboard).

```
hackwithhyderbad/
├── backend/                       # Python FastAPI Backend & Hindsight AI Memory Engine
│   ├── ai_memory_agent/          # Core AI agents, memory engines, models, & API routes
│   │   ├── agents/               # Investigation, Compliance, Audit & Memory Orchestrators
│   │   ├── api/                  # FastAPI routes & CORS server configuration
│   │   ├── memory/               # Hindsight biomimetic engine & hybrid similarity search
│   │   ├── intelligence/         # Automated RCA & Post-Mortem generators
│   │   └── llm/                  # Gemini, OpenAI, & offline expert security models
│   ├── data/                     # Baseline security controls & local memory snapshots
│   ├── demo/                     # 10-step automated story & CLI runner
│   ├── tests/                    # Automated Pytest suite (11/11 passing)
│   ├── main.py                   # Server, Demo, and CLI launcher
│   ├── requirements.txt          # Backend Python dependencies
│   ├── Dockerfile                # Backend container configuration
│   └── AI_TEAM_HANDOFF.md        # Workstream handoff documentation
│
└── frontend/                      # React + Vite + TypeScript Web Dashboard
    ├── src/
    │   ├── components/           # Dashboard, Triage, Memory Explorer & Auditor Portal
    │   ├── services/             # REST API Client for FastAPI backend
    │   ├── types/                # TypeScript data schemas
    │   ├── App.tsx               # Main application container
    │   └── index.css             # Glassmorphism dark-theme design system
    ├── index.html                # Entry document
    ├── package.json              # Frontend npm dependencies
    └── vite.config.ts            # Vite build configuration
```

---

## 🧠 Why Hindsight? The 4 Biomimetic Memory Networks

| Memory Network | Cognitive Role | Example in this System |
|---|---|---|
| **World Network** | Objective facts, baselines & standards | SOC 2 / NIST CSF control baselines, policy rules |
| **Experience Network** | Episodic history of specific actions taken | Incident #1024 investigation, RCA, remediation steps |
| **Observation Network** | Patterns synthesized across multiple incidents | "Repeated S3 exposure incidents detected across cloud assets" |
| **Opinion Network** | Evolving organizational beliefs & risks | "Access policies carry high manual error rate; enforce automated guardrails" |

---

## 🚀 Quickstart Guide

### 1. Launching the Backend API Server
Navigate to the `backend/` directory:
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .

# Start FastAPI server on port 8000
python main.py server --port 8000
```
- Interactive OpenAPI Swagger Docs: **[http://localhost:8000/docs](http://localhost:8000/docs)**
- Health Endpoint: **[http://localhost:8000/api/health](http://localhost:8000/api/health)**

To run backend tests:
```bash
pytest -v
```

### 2. Launching the Frontend Dashboard
Navigate to the `frontend/` directory:
```bash
cd frontend
npm install
npm run dev
```
- Web Dashboard URL: **[http://localhost:5173](http://localhost:5173)**

---

## 📡 Key REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/incidents/investigate` | Ingests incident, conducts AI RCA, maps controls, fingerprints evidence, retains to Hindsight |
| `GET` | `/api/incidents` | Lists all investigated incidents with recurrence status |
| `GET` | `/api/incidents/{incident_id}` | Detailed incident investigation, timeline, and post-mortem |
| `POST` | `/api/audit/query` | Auditor inquiry against Hindsight memory (e.g. Access Control findings) |
| `GET` | `/api/memory/recall` | Hybrid semantic search across Hindsight memory bank |
| `GET` | `/api/memory/reflect` | Reflects over memory to extract recurring patterns and risk posture |
| `GET` | `/api/memory/networks` | Live memory unit count across World, Experience, Observation, Opinion |
| `GET` | `/api/memory/timeline` | Chronological security knowledge timeline |
| `POST` | `/api/demo/run-story` | Runs the full 10-step demo story via API |
| `GET` | `/api/health` | Health check for memory engine and LLM provider |
# Devops
