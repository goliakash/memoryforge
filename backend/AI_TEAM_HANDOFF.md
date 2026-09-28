# 🧠 AI Security Operations & Compliance Memory Agent — Team Handoff Document

> **Focus Workstream**: AI Topics (Member 1: Security Investigation + Member 2: Hindsight Memory + Member 3: Compliance & Audit + AI Orchestration)

---

## 📌 Executive Summary

This codebase delivers the complete **AI and Memory Core** for the **Security Operations & Compliance Memory Agent**. It implements the principle: **"The memory loop is the product."**

Instead of treating Hindsight like a generic vector database, it establishes structured **organizational memory** across four biomimetic networks (**World, Experience, Observation, Opinion**). It powers automated incident investigation, root cause discovery, security control mapping, cryptographic evidence packaging, and audit inquiry answering.

---

## 🏗️ Architecture & Component Mapping

```
                                  USER / AUDITOR
                                        ↓
                       Web Dashboard (Member 4: Frontend)
                                        ↓
                       FastAPI Backend (FastAPI / Swagger)
                                        ↓
        ┌───────────────────────────────┼───────────────────────────────┐
        ↓                               ↓                               ↓
   Member 1:                        Member 3:                       Member 3:
Incident Agent                   Compliance Agent                  Audit Agent
(Triage, RCA, Post-Mortem)       (Controls, Remediation, Ev.)      (Audit Synthesis)
        └───────────────────────────────┬───────────────────────────────┘
                                        ↓
                         AI Orchestrator (Memory Loop)
                                        ↓
                        HINDSIGHT MEMORY ENGINE 🧠
             ┌───────────────┬─────────────────┬──────────────┐
             ↓               ↓                 ↓              ↓
       World Network  Experience Network  Observation Network  Opinion Network
       (Gov/Controls) (Incident History)   (Recurring Trends)  (Beliefs/Risks)
```

---

## 👥 How Team Members Interface With This AI Core

### 🎨 Member 4: Frontend / UX Developer
You have a fully operational, CORS-enabled REST API ready to power the dashboard.

- **Start Backend API Server**:
  ```bash
  python main.py server --port 8000
  ```
- **Interactive Swagger Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Key Endpoints for Frontend**:
  1. `POST /api/incidents/investigate`: Submit a new incident. Returns the full investigation, root cause, mapped controls, remediation runbooks, evidence hashes, and whether this was a **recurring incident** with prior memory recalled.
  2. `GET /api/incidents`: List all investigated incidents.
  3. `GET /api/incidents/{incident_id}`: Fetch post-mortem, timeline, and audit evidence for an incident.
  4. `POST /api/audit/query`: Auditor enters e.g. "Access Control" and question. Returns audit findings, compliance posture (`COMPLIANT_WITH_REMEDIATION_EVIDENCE`), and SHA-256 evidence links.
  5. `GET /api/memory/networks`: Returns counts for World, Experience, Observation, and Opinion networks (for your memory visualization cards!).
  6. `GET /api/memory/timeline`: Returns the chronological memory stream.
  7. `POST /api/demo/run-story`: Executes the 10-step demo story and returns all steps as structured JSON for a one-click automated demo button!

---

### 🛡️ Member 5: Integration & DevSecOps
The AI core is 100% container-ready, zero-dependency by default (local embedded Hindsight engine), and fully tested.

- **Run Test Suite**:
  ```bash
  pytest -v
  ```
  *(11 tests passing: memory retain/recall/reflect, investigation RCA, compliance mapping, SHA-256 hashing, audit retrieval, and orchestrator memory loop)*

- **Docker Build**:
  ```bash
  docker build -t secops-memory-agent:1.0.0 .
  ```
- **Docker Run**:
  ```bash
  docker run -p 8000:8000 secops-memory-agent:1.0.0
  ```
- **Environment Variables**:
  Copy `.env.example` to `.env`. It supports:
  - `LLM_PROVIDER`: `auto` (default), `gemini`, `openai`, or `expert` (offline deterministic).
  - `HINDSIGHT_API_KEY` & `HINDSIGHT_BASE_URL`: If connecting to a live Hindsight Cloud instance or external Docker server; if unset, it automatically operates in the embedded biomimetic mode.

---

### 🔍 Member 1, 2, 3: Investigation, Memory & Compliance Leads

| Module | File Location | Key Class / Functions |
|---|---|---|
| **Incident Investigation Agent** | `ai_memory_agent/agents/investigation_agent.py` | `SecurityInvestigationAgent.investigate()`, `recall_prior_incidents()` |
| **Hindsight Memory Engine** | `ai_memory_agent/memory/local_hindsight.py` & `hindsight_adapter.py` | `HindsightAdapter.retain()`, `recall()`, `reflect()` |
| **Hybrid Similarity Engine** | `ai_memory_agent/memory/similarity.py` | `calculate_hybrid_similarity()` (query coverage + cosine + entities) |
| **Compliance & Controls Agent** | `ai_memory_agent/agents/compliance_agent.py` | `ComplianceAgent.map_security_controls()`, `organize_and_fingerprint_evidence()` |
| **Audit Agent** | `ai_memory_agent/agents/audit_agent.py` | `AuditAgent.process_audit_request()` |
| **Central Orchestrator** | `ai_memory_agent/agents/orchestrator.py` | `SecurityMemoryOrchestrator.investigate_and_remember()`, `run_demo_story()` |

---

## 🎬 The 10-Step Demo Story Walkthrough

To run the complete live demo with rich terminal visuals:
```bash
python main.py demo
```

Here is the exact storyline executed:
1. **Step 1 (Incident #1024)**: Ingest `customer-data-bucket` exposure.
2. **Step 2 (AI Investigation)**: AI Agent determines Root Cause: *Access Policy Misconfiguration*.
3. **Step 3 (Controls & Remediation)**: Maps SOC2-CC6.1, NIST-PR.AC-04, ISO-A.5.15. Generates remediation plan and SHA-256 evidence fingerprints.
4. **Step 4 (Hindsight Retain)**: Preserves incident learnings into Hindsight Experience Network.
5. **Step 5 (Incident #1038)**: New similar incident occurs on `analytics-data-bucket`.
6. **Step 6 (Hindsight Recall 🧠)**: Agent recalls Incident #1024 (similarity score > 0.45).
7. **Step 7 (Knowledge Reuse)**: Agent flags *Recurring Pattern*, reuses proven remediation playbook, and links prior post-mortem.
8. **Step 8 (Auditor Request)**: External auditor asks for historical access-control findings and evidence.
9. **Step 9 (Audit Retrieval)**: Agent queries Hindsight memory, retrieves historical findings from both incidents.
10. **Step 10 (Audit Evidence Package)**: Delivers complete report with cryptographic verification hashes, 100% remediation rate, and preventive control guidance.
