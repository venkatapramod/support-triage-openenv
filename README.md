---
title: Support Triage Env
emoji: 🎫
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
tags:
  - openenv
---
# 🎫 Support Ticket Triage Environment

A real-world OpenEnv environment where an AI agent triages customer support tickets by categorizing them, assigning priority levels, routing to the correct department, and suggesting responses.

## Why This Environment?

Customer support triage is a high-impact, real-world task performed millions of times daily across industries. Getting it right means faster resolution times, happier customers, and lower operational costs. Getting it wrong means escalations, churn, and lost revenue.

This environment challenges an AI agent to make **four decisions** per ticket under realistic conditions — ambiguous language, multi-issue tickets, varying customer tiers, and time-sensitive situations.

## 🎯 What This Demonstrates

- **Environment design** — custom OpenEnv-compliant environment with structured action space, observation space, reward function, and episode state management
- **Production API** — FastAPI server with `/health`, `/reset`, `/step`, `/state`, `/schema`, and `/tasks` endpoints; OpenAPI docs auto-generated at `/docs`
- **Reward engineering** — multi-component scoring (category 35%, priority 25%, department 30%, response quality 10%) with partial credit for adjacent priority levels
- **Evaluation methodology** — 27 hand-crafted tickets across 3 difficulty tiers, designed to test single-issue vs. multi-issue reasoning
- **LLM benchmarking** — inference harness against Qwen2.5-72B-Instruct via Hugging Face, with structured logging
- **Engineering rigor** — Pydantic models, Docker containerization, retry logic with max-attempts cap, automated pre-submission validator with 30+ checks

## Tasks

| Task | Difficulty | Tickets | Description |
|------|-----------|---------|-------------|
| `easy_triage` | Easy | 8 | Straightforward tickets with obvious categories — "I was charged twice", "app crashes on settings", "package arrived damaged" |
| `medium_triage` | Medium | 9 | Ambiguous tickets where category/priority/department require careful reasoning — billing symptoms masking technical issues, mixed shipping+refund requests, account lifecycle vs. billing |
| `hard_triage` | Hard | 10 | Complex multi-issue tickets requiring nuanced judgment — simultaneous SSO + admin + export failures, GDPR deletion requests, SOC2 audit failures, disputed sales promises |

## Baseline Results

Tested with `Qwen/Qwen2.5-72B-Instruct` via Hugging Face Inference:

| Task | Tickets | Avg Score | Description |
|------|---------|-----------|-------------|
| easy_triage | 8 | ~0.80 | Simple tickets, occasional priority/dept misses |
| medium_triage | 9 | ~0.72 | Ambiguous categories trip up naive classification |
| hard_triage | 10 | ~0.68 | Multi-issue tickets with competing categorizations |

**27 total tickets** across 3 difficulty levels.

## Action Space

The agent submits a JSON object with four fields:

```json
{
    "category": "billing | technical | account | shipping | general",
    "priority": "critical | high | medium | low",
    "department": "engineering | finance | logistics | customer_success | admin",
    "suggested_response": "A brief professional response to the customer"
}
```

**Categories:** billing (payments, charges, invoices), technical (bugs, crashes, APIs, security), account (login, access, migrations), shipping (delivery, tracking, packages), general (how-to, feature requests)

**Priority Levels:** critical (outages, breaches, legal deadlines), high (functionality broken, paying customer blocked), medium (workaround exists), low (general questions)

**Departments:** engineering, finance, logistics, customer_success, admin

## Observation Space

```json
{
    "ticket_id": "string",
    "ticket_subject": "string",
    "ticket_body": "string",
    "customer_name": "string",
    "customer_tier": "free | pro | enterprise",
    "feedback": "string (grading feedback from last action)",
    "tickets_remaining": "integer",
    "last_action_error": "string | null",
    "done": "boolean",
    "reward": "float (0.0-1.0)"
}
```

## Reward Function

Each ticket is scored on a 0.0–1.0 scale with partial credit:

| Component | Weight | Scoring |
|-----------|--------|---------|
| Category | 35% | Exact match required |
| Priority | 25% | Exact match = 25%, adjacent level = 10% |
| Department | 30% | Exact match required |
| Response Quality | 10% | Bonus for relevant, substantive responses |

**Partial credit example:** If a ticket's true priority is "critical" and the agent assigns "high" (one level off), it earns 10% instead of 0% for that component.

**Invalid actions** (wrong enum values) receive 0.0 reward and the agent can retry up to 3 times per ticket before it's skipped.

## Sample Inference Output

```
[START] task=easy_triage env=support_triage_env model=Qwen/Qwen2.5-72B-Instruct
[STEP] step=1 action=triage(cat=billing,pri=high,dept=finance) reward=0.90 done=false error=null
[STEP] step=2 action=triage(cat=account,pri=medium,dept=customer_success) reward=0.70 done=false error=null
...
[END] success=true steps=8 score=0.800 rewards=0.90,0.70,0.95,0.85,0.65,0.85,0.70,0.80
```

## Setup Instructions

### Install Dependencies

```bash
pip install openenv-core fastapi uvicorn pydantic openai requests
```

### Test Locally (No API Key Needed)

```python
from server.triage_environment import SupportTriageEnvironment
from models import TriageAction

env = SupportTriageEnvironment(task_name='easy_triage')
obs = env.reset(seed=42)
print('Ticket:', obs.ticket_subject)

action = TriageAction(
    category='billing', priority='high', department='finance',
    suggested_response='We will refund the duplicate charge immediately.'
)
obs = env.step(action)
print('Reward:', obs.reward)
print('Feedback:', obs.feedback)
```

### Run the Server

```bash
python -m uvicorn server.app:app --host 0.0.0.0 --port 7860
```

### Run Inference with LLM

```bash
export HF_TOKEN="your-api-key"
export API_BASE_URL="https://router.huggingface.co/v1"
export MODEL_NAME="Qwen/Qwen2.5-72B-Instruct"
python inference.py
```

### Docker

```bash
docker build -t support-triage-env .
docker run -p 7860:7860 support-triage-env
```

## 🔨 What I Built

The OpenEnv framework provides the base `Environment` class and HTTP server scaffolding. Everything below is original work for this project:

- **Domain dataset** (`tickets.py`) — 27 hand-crafted support tickets across easy/medium/hard tiers
- **Triage environment** (`server/triage_environment.py`) — episode lifecycle, multi-component reward function with partial credit, retry-with-skip logic for invalid actions, structured per-step feedback
- **Reward function** — weighted scoring across category, priority, department, and response quality with adjacent-priority partial credit
- **FastAPI application** (`server/app.py`) — REST endpoints, environment factory, task selection via env vars
- **Inference harness** (`inference.py`) — OpenAI-compatible client with structured `[START]/[STEP]/[END]` logging
- **Validation suite** (`validate.py`) — 30+ programmatic checks covering file structure, API contract, reward bounds, and server health
- **Container & deployment** — Dockerfile with health check, `openenv.yaml` manifest

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/reset` | POST | Start new episode, returns first ticket |
| `/step` | POST | Submit triage action, returns next ticket |
| `/state` | GET | Current episode state |
| `/schema` | GET | Action/observation JSON schemas |
| `/tasks` | GET | List available tasks |
| `/docs` | GET | Swagger UI |

## Project Structure

```
support_triage_env/
├── inference.py               # Baseline inference script (root)
├── models.py                  # Action, Observation, State Pydantic models
├── tickets.py                 # 27 hand-crafted tickets across 3 difficulty levels
├── openenv.yaml               # OpenEnv manifest
├── Dockerfile                 # Container for HF Spaces
├── pyproject.toml             # Python package config
├── validate.py                # Pre-submission validation
├── README.md
├── __init__.py
└── server/
    ├── __init__.py
    ├── app.py                 # FastAPI application
    ├── triage_environment.py  # Core environment logic
    └── requirements.txt
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `API_BASE_URL` | No | `https://router.huggingface.co/v1` | LLM API endpoint |
| `MODEL_NAME` | No | `Qwen/Qwen2.5-72B-Instruct` | Model identifier |
| `HF_TOKEN` | Yes | — | API key (no default) |
| `TRIAGE_TASK` | No | `easy_triage` | Task to load on server |

## Design Decisions

- **27 hand-crafted tickets** rather than synthetic data — each ticket is realistic and tests specific triage skills
- **Partial credit scoring** — adjacent priority levels get partial reward, encouraging the agent to learn the priority spectrum
- **Max attempts per ticket** — invalid actions get 3 retries before the ticket is skipped, preventing infinite loops
- **All rewards in [0.0, 1.0]** — no negative rewards, compliant with OpenEnv spec

## Scope

- Prototype-scale dataset (27 tickets) demonstrating environment architecture and reward design
- Single-label routing for simplicity and reproducibility

## License

MIT
