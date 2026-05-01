# Support Ticket Triage Environment - Server Implementation

import uuid
import random
from typing import Optional, Any, List, Dict

from openenv.core.env_server import Environment

try:
    from ..models import TriageAction, TriageObservation, TriageState
    from ..tickets import TASK_CONFIGS
except ImportError:
    from models import TriageAction, TriageObservation, TriageState
    from tickets import TASK_CONFIGS


VALID_CATEGORIES = {"billing", "technical", "account", "shipping", "general"}
VALID_PRIORITIES = {"critical", "high", "medium", "low"}
VALID_DEPARTMENTS = {"engineering", "finance", "logistics", "customer_success", "admin"}


MAX_ATTEMPTS_PER_TICKET = 3


class SupportTriageEnvironment(Environment[TriageAction, TriageObservation, TriageState]):
    """
    An environment where an AI agent triages customer support tickets.

    The agent must read each ticket and decide:
    1. Category (billing, technical, account, shipping, general)
    2. Priority (critical, high, medium, low)
    3. Department to route to (engineering, finance, logistics, customer_success, admin)
    4. Suggest a brief response

    Rewards are based on accuracy of categorization, priority assignment,
    department routing, and quality of suggested response.

    Invalid actions receive 0.0 reward and the agent gets another attempt.
    After MAX_ATTEMPTS_PER_TICKET failed attempts, the ticket is skipped with 0.0 reward.
    Episode ends when all tickets are triaged or max total steps exceeded.
    """

    SUPPORTS_CONCURRENT_SESSIONS = True

    def __init__(self, task_name: str = "easy_triage"):
        super().__init__()
        self._task_name = task_name
        self._state = TriageState()
        self._tickets: List[Dict[str, Any]] = []
        self._current_ticket_idx: int = 0
        self._rewards: List[float] = []
        self._attempts_on_current: int = 0
        self._max_total_steps: int = 0

    def reset(
        self,
        seed: Optional[int] = None,
        episode_id: Optional[str] = None,
        **kwargs: Any,
    ) -> TriageObservation:
        """Reset environment and present the first ticket."""
        if seed is not None:
            random.seed(seed)

        task_config = TASK_CONFIGS.get(self._task_name)
        if task_config is None:
            task_config = TASK_CONFIGS["easy_triage"]

        self._tickets = task_config["tickets_fn"]()
        self._current_ticket_idx = 0
        self._rewards = []
        self._attempts_on_current = 0
        self._max_total_steps = len(self._tickets) * MAX_ATTEMPTS_PER_TICKET

        ep_id = episode_id or str(uuid.uuid4())

        self._state = TriageState(
            episode_id=ep_id,
            step_count=0,
            task_name=self._task_name,
            total_tickets=len(self._tickets),
            tickets_triaged=0,
            cumulative_reward=0.0,
            correct_categories=0,
            correct_priorities=0,
            correct_departments=0,
            response_quality_sum=0.0,
        )

        ticket = self._tickets[0]
        return TriageObservation(
            done=False,
            reward=0.0,
            ticket_id=ticket["id"],
            ticket_subject=ticket["subject"],
            ticket_body=ticket["body"],
            customer_name=ticket["customer_name"],
            customer_tier=ticket["customer_tier"],
            feedback="New triage session started. Please categorize this ticket.",
            tickets_remaining=len(self._tickets) - 1,
            last_action_error=None,
        )

    def step(
        self,
        action: TriageAction,
        timeout_s: Optional[float] = None,
        **kwargs: Any,
    ) -> TriageObservation:
        """Process the agent's triage decision and present the next ticket."""
        self._state.step_count += 1
        self._attempts_on_current += 1

       
        if self._state.step_count > self._max_total_steps:
            self._rewards.append(0.0)
            return TriageObservation(
                done=True,
                reward=0.0,
                ticket_id="",
                ticket_subject="",
                ticket_body="",
                customer_name="",
                customer_tier="",
                feedback="Episode terminated: maximum steps exceeded.",
                tickets_remaining=0,
                last_action_error="Max steps exceeded",
            )

        
        error = None
        if action.category not in VALID_CATEGORIES:
            error = f"Invalid category '{action.category}'. Must be one of: {sorted(VALID_CATEGORIES)}"
        elif action.priority not in VALID_PRIORITIES:
            error = f"Invalid priority '{action.priority}'. Must be one of: {sorted(VALID_PRIORITIES)}"
        elif action.department not in VALID_DEPARTMENTS:
            error = f"Invalid department '{action.department}'. Must be one of: {sorted(VALID_DEPARTMENTS)}"

        if error:
            # Invalid action: 0.0 reward
            self._rewards.append(0.0)
            ticket = self._tickets[self._current_ticket_idx]

            # If too many attempts on same ticket, skip it
            if self._attempts_on_current >= MAX_ATTEMPTS_PER_TICKET:
                self._state.tickets_triaged += 1
                self._current_ticket_idx += 1
                self._attempts_on_current = 0
                is_done = self._current_ticket_idx >= len(self._tickets)

                if is_done:
                    return TriageObservation(
                        done=True,
                        reward=0.0,
                        ticket_id=ticket["id"],
                        ticket_subject="",
                        ticket_body="",
                        customer_name="",
                        customer_tier="",
                        feedback=f"Skipped ticket after {MAX_ATTEMPTS_PER_TICKET} failed attempts. Episode complete.",
                        tickets_remaining=0,
                        last_action_error=error,
                    )

                next_ticket = self._tickets[self._current_ticket_idx]
                return TriageObservation(
                    done=False,
                    reward=0.0,
                    ticket_id=next_ticket["id"],
                    ticket_subject=next_ticket["subject"],
                    ticket_body=next_ticket["body"],
                    customer_name=next_ticket["customer_name"],
                    customer_tier=next_ticket["customer_tier"],
                    feedback=f"Ticket skipped after {MAX_ATTEMPTS_PER_TICKET} invalid attempts. Moving to next ticket.",
                    tickets_remaining=len(self._tickets) - self._current_ticket_idx - 1,
                    last_action_error=error,
                )

            return TriageObservation(
                done=False,
                reward=0.0,
                ticket_id=ticket["id"],
                ticket_subject=ticket["subject"],
                ticket_body=ticket["body"],
                customer_name=ticket["customer_name"],
                customer_tier=ticket["customer_tier"],
                feedback=f"Invalid action: {error}. Attempt {self._attempts_on_current}/{MAX_ATTEMPTS_PER_TICKET}.",
                tickets_remaining=len(self._tickets) - self._current_ticket_idx - 1,
                last_action_error=error,
            )


        ticket = self._tickets[self._current_ticket_idx]
        gt = ticket["ground_truth"]
        reward = self._compute_reward(action, gt, ticket)

        # Update state
        self._state.tickets_triaged += 1
        self._state.cumulative_reward += reward
        self._rewards.append(reward)
        self._attempts_on_current = 0

        if action.category == gt["category"]:
            self._state.correct_categories += 1
        if action.priority == gt["priority"]:
            self._state.correct_priorities += 1
        if action.department == gt["department"]:
            self._state.correct_departments += 1

       
        feedback_parts = []
        if action.category == gt["category"]:
            feedback_parts.append("Category: CORRECT")
        else:
            feedback_parts.append(f"Category: INCORRECT (was '{action.category}', expected '{gt['category']}')")
        if action.priority == gt["priority"]:
            feedback_parts.append("Priority: CORRECT")
        else:
            feedback_parts.append(f"Priority: INCORRECT (was '{action.priority}', expected '{gt['priority']}')")
        if action.department == gt["department"]:
            feedback_parts.append("Department: CORRECT")
        else:
            feedback_parts.append(f"Department: INCORRECT (was '{action.department}', expected '{gt['department']}')")
        feedback_parts.append(f"Step reward: {reward:.2f}")
        feedback = " | ".join(feedback_parts)

        # Move to next ticket
        self._current_ticket_idx += 1
        is_done = self._current_ticket_idx >= len(self._tickets)

        if is_done:
            final_score = self._state.cumulative_reward / self._state.total_tickets
            feedback += f" | Episode complete! Final score: {final_score:.2f}"
            return TriageObservation(
                done=True,
                reward=reward,
                ticket_id=ticket["id"],
                ticket_subject="",
                ticket_body="",
                customer_name="",
                customer_tier="",
                feedback=feedback,
                tickets_remaining=0,
                last_action_error=None,
            )

        # Present next ticket
        next_ticket = self._tickets[self._current_ticket_idx]
        return TriageObservation(
            done=False,
            reward=reward,
            ticket_id=next_ticket["id"],
            ticket_subject=next_ticket["subject"],
            ticket_body=next_ticket["body"],
            customer_name=next_ticket["customer_name"],
            customer_tier=next_ticket["customer_tier"],
            feedback=feedback,
            tickets_remaining=len(self._tickets) - self._current_ticket_idx - 1,
            last_action_error=None,
        )

    def _compute_reward(self, action: TriageAction, ground_truth: Dict, ticket: Dict) -> float:
        """
        Compute reward for a single triage action.

        Scoring breakdown:
        - Category correct: 0.35
        - Priority correct: 0.25 (adjacent: 0.10)
        - Department correct: 0.30
        - Response quality bonus: up to 0.10

        Total possible: 1.0
        All rewards are in [0.0, 1.0].
        """
        reward = 0.0

        
        if action.category == ground_truth["category"]:
            reward += 0.35

       
        priority_order = ["low", "medium", "high", "critical"]
        if action.priority == ground_truth["priority"]:
            reward += 0.25
        else:
            
            try:
                pred_idx = priority_order.index(action.priority)
                true_idx = priority_order.index(ground_truth["priority"])
                if abs(pred_idx - true_idx) == 1:
                    reward += 0.10
            except ValueError:
                pass

       
        if action.department == ground_truth["department"]:
            reward += 0.30

       
        if action.suggested_response and len(action.suggested_response.strip()) > 10:
            response_lower = action.suggested_response.lower()
            subject_lower = ticket["subject"].lower()
            body_lower = ticket["body"].lower()

            
            key_words = set(subject_lower.split()) | set(body_lower.split()[:20])
            key_words = {w for w in key_words if len(w) > 4}
            matches = sum(1 for w in key_words if w in response_lower)
            if matches >= 3:
                reward += 0.10
            elif matches >= 1:
                reward += 0.05

            self._state.response_quality_sum += min(0.10, max(0, reward - 0.90))

        
        return max(0.0, min(reward, 1.0))

    def close(self):
        """Clean up resources when the episode ends."""
        self._tickets = []
        self._rewards = []
        self._current_ticket_idx = 0

    @property
    def state(self) -> TriageState:
        return self._state
