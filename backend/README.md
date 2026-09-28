# 🧠 AI Security Operations & Compliance Memory Agent
### *Persistent Organizational Memory for SecOps and Compliance Powered by Hindsight*

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-green.svg)](https://fastapi.tiangolo.com)
[![Tests Passing](https://img.shields.io/badge/Tests-11%20Passed-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

---

## 🎯 The Core Problem

Security teams investigate incidents every day, but the knowledge gained from those investigations — root causes, affected controls, remediation playbooks, evidence, and post-mortems — often gets buried in closed tickets and siloed documents.

When a similar incident recurs, engineers start from scratch, and auditors spend weeks tracking down historical proof.

**This system solves that by turning episodic security investigations into persistent organizational memory.**

```
Security Incident
       ↓
AI Investigation
       ↓
Root Cause
       ↓
Security Control
       ↓
Remediation
       ↓
Evidence (SHA-256)
       ↓
Post-Mortem
       ↓
Hindsight Memory 🧠 (World, Experience, Observation, Opinion)
       ↓
Future Incident / Audit
       ↓
Recall Previous Knowledge
       ↓
Instant Investigation Acceleration / Continuous Audit Readiness
```

---

## 🧠 Why Hindsight? The 4 Biomimetic Memory Networks

Rather than a simple vector store or raw text lookup, Hindsight structures knowledge across four cognitive networks:

| Memory Network | Cognitive Role | Example in this System |
|---|---|---|
| **World Network** | Objective facts, baselines & standards | SOC 2 / NIST CSF control baselines, policy rules |
| **Experience Network** | Episodic history of specific actions taken | Incident #1024 investigation, RCA, remediation steps |
| **Observation Network** | Patterns synthesized across multiple incidents | "Repeated S3 exposure incidents detected across cloud assets" |
| **Opinion Network** | Evolving organizational beliefs & risks | "Access policies carry high manual error rate; enforce automated guardrails" |

---

## 🚀 Quickstart

### 1. Installation
Clone the repository and install dependencies:
```bash
pip install -e .
```

### 2. Run the 10-Step Automated Demo Story
Run the terminal-visualized demo showing Incident #1024 investigation, retention into Hindsight, Incident #1038 recall, and Auditor query:
```bash
python main.py demo
```

### 3. Launch Interactive Terminal CLI
Test custom incidents, queries, and memory inspections:
```bash
python main.py cli
```

### 4. Start the FastAPI REST Backend
Power the frontend dashboard with interactive Swagger documentation:
```bash
python main.py server --port 8000
```
Visit **[http://localhost:8000/docs](http://localhost:8000/docs)** to test all REST endpoints.

---

## 🧪 Running the Automated Test Suite

```bash
pytest -v
```
All 11 unit and integration tests validate:
- Hindsight Memory Network operations (`retain`, `recall`, `reflect`)
- Incident investigation & Root-Cause Analysis (RCA)
- Prior incident correlation and recurrence detection
- Security control mapping (SOC 2 CC6.1, NIST PR.AC-04, ISO 27001 A.5.15)
- Remediation playbook synthesis and SHA-256 evidence fingerprinting
- Auditor query processing and compliance report synthesis
- Complete end-to-end memory loop orchestrator

---

## 📡 REST API Reference

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

---

## 👥 Team Workstream Handoff

Please consult **[AI_TEAM_HANDOFF.md](file:///d:/hackwithhyderbad/AI_TEAM_HANDOFF.md)** for detailed integration guidance:
- **Member 4 (Frontend)**: JSON schemas, endpoints, and CORS configuration.
- **Member 5 (DevSecOps)**: Docker build instructions, CI/CD test commands, and environment settings.
