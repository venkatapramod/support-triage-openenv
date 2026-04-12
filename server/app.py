# Support Ticket Triage Environment - FastAPI Application

import os
from openenv.core.env_server import create_fastapi_app

try:
    from ..models import TriageAction, TriageObservation
    from .triage_environment import SupportTriageEnvironment
except ImportError:
    from models import TriageAction, TriageObservation
    from server.triage_environment import SupportTriageEnvironment


def create_env():
    """Factory function to create a new environment instance."""
    task = os.environ.get("TRIAGE_TASK", "easy_triage")
    return SupportTriageEnvironment(task_name=task)


app = create_fastapi_app(
    env=create_env,
    action_cls=TriageAction,
    observation_cls=TriageObservation,
)


@app.get("/health")
async def health():
    return {"status": "healthy", "environment": "support_triage_env"}


@app.get("/tasks")
async def list_tasks():
    from tickets import TASK_CONFIGS
    return {
        name: {"description": cfg["description"], "num_tickets": cfg["num_tickets"]}
        for name, cfg in TASK_CONFIGS.items()
    }


def main():
    """Entry point for the server."""
    import uvicorn
    port = int(os.environ.get("PORT", "7860"))
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
