
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
from openenv.core.env_server.types import Action, Observation, State
from pydantic import Field


class TriageAction(Action):
    """Agent's triage decision for a support ticket."""
    category: str = Field(
        description="Ticket category: billing, technical, account, shipping, general"
    )
    priority: str = Field(
        description="Priority level: critical, high, medium, low"
    )
    department: str = Field(
        description="Routing department: engineering, finance, logistics, customer_success, admin"
    )
    suggested_response: str = Field(
        default="",
        description="A brief suggested response or next action for the ticket"
    )


class TriageObservation(Observation):
    """Observation returned after each triage action or on reset."""
    ticket_id: str = Field(default="", description="Current ticket ID")
    ticket_subject: str = Field(default="", description="Ticket subject line")
    ticket_body: str = Field(default="", description="Full ticket message body")
    customer_name: str = Field(default="", description="Customer name")
    customer_tier: str = Field(default="", description="Customer tier: free, pro, enterprise")
    feedback: str = Field(default="", description="Feedback on last triage action")
    tickets_remaining: int = Field(default=0, description="Number of tickets left in episode")
    last_action_error: Optional[str] = Field(default=None, description="Error message if action was invalid")


class TriageState(State):
    """Internal state of the triage environment."""
    task_name: str = Field(default="", description="Current task name")
    total_tickets: int = Field(default=0, description="Total tickets in this episode")
    tickets_triaged: int = Field(default=0, description="Tickets triaged so far")
    cumulative_reward: float = Field(default=0.0, description="Total reward accumulated")
    correct_categories: int = Field(default=0, description="Number of correct categorizations")
    correct_priorities: int = Field(default=0, description="Number of correct priority assignments")
    correct_departments: int = Field(default=0, description="Number of correct department routings")
    response_quality_sum: float = Field(default=0.0, description="Sum of response quality scores")
