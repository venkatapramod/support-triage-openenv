#!/usr/bin/env python3
"""
Inference script for Support Ticket Triage Environment.

Uses an LLM to triage customer support tickets via the OpenEnv environment.

Required environment variables:
    API_BASE_URL       - LLM API endpoint (default: https://router.huggingface.co/v1)
    MODEL_NAME         - Model identifier (default: Qwen/Qwen2.5-72B-Instruct)
    HF_TOKEN           - Hugging Face / API key (required, no default)
    LOCAL_IMAGE_NAME   - Docker image name for the environment (optional, for from_docker_image)
"""

import asyncio
import os
import sys
import json
import textwrap
from typing import List, Optional

from openai import OpenAI

# ── Environment Variables ────────────────────────────────────────────────────
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
HF_TOKEN = os.getenv("HF_TOKEN")
IMAGE_NAME = os.getenv("LOCAL_IMAGE_NAME")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

# ── OpenAI Client ────────────────────────────────────────────────────────────
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN,
)

# ── Environment Config ───────────────────────────────────────────────────────
ENV_NAME = "support_triage_env"
MAX_STEPS = 30  # Safety limit across all tickets in a task
TEMPERATURE = 0.1
MAX_TOKENS = 500

SYSTEM_PROMPT = textwrap.dedent("""
    You are an expert customer support triage agent. You will receive a customer
    support ticket and must decide:

    1. **Category**: One of: billing, technical, account, shipping, general
    2. **Priority**: One of: critical, high, medium, low
    3. **Department**: One of: engineering, finance, logistics, customer_success, admin
    4. **Suggested Response**: A brief, professional response addressing the customer's concern.

    Guidelines for categorization:
    - billing: payment issues, charges, invoices, pricing, refunds, subscriptions
    - technical: bugs, crashes, errors, performance, integrations, API issues, security
    - account: login, access, permissions, account management, data requests, migrations
    - shipping: delivery, tracking, lost/damaged packages, address issues
    - general: how-to questions, feature requests, documentation, general inquiries

    Guidelines for priority:
    - critical: service outage affecting many users, security breach, legal/compliance
      deadlines, enterprise customer with urgent business impact
    - high: significant functionality broken, paying customer blocked, data issues
    - medium: inconvenience but workaround exists, standard requests from paying customers
    - low: general questions, feature requests, non-urgent informational inquiries

    Guidelines for department routing:
    - engineering: bugs, crashes, performance, security, API issues, integrations
    - finance: billing, payments, invoices, pricing, refunds, credits
    - logistics: shipping, delivery, tracking, packages, returns
    - customer_success: account management, onboarding, migrations, access issues, general help
    - admin: legal, compliance, GDPR, policy, administrative matters

    You MUST respond with ONLY a valid JSON object in this exact format:
    {
        "category": "<category>",
        "priority": "<priority>",
        "department": "<department>",
        "suggested_response": "<brief professional response>"
    }

    Do NOT include any text outside the JSON object. No markdown, no explanation.
""").strip()


# ── Logging helpers ──────────────────────────────────────────────────────────

def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: List[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}", flush=True)


# ── LLM call ─────────────────────────────────────────────────────────────────

def call_llm(ticket_subject: str, ticket_body: str, customer_name: str, customer_tier: str) -> dict:
    """Call the LLM to triage a ticket. Returns parsed action dict."""
    user_message = (
        f"Please triage this support ticket:\n\n"
        f"**Ticket Subject:** {ticket_subject}\n"
        f"**Customer:** {customer_name} ({customer_tier} tier)\n"
        f"**Message:**\n{ticket_body}\n\n"
        f"Respond with ONLY the JSON object containing category, priority, "
        f"department, and suggested_response."
    )

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
            stream=False,
        )
        content = (response.choices[0].message.content or "").strip()

        # Strip markdown code fences if present
        if content.startswith("```"):
            content = content.split("\n", 1)[1] if "\n" in content else content[3:]
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()
        if content.startswith("json"):
            content = content[4:].strip()

        return json.loads(content)
    except (json.JSONDecodeError, Exception) as exc:
        print(f"[DEBUG] LLM parse error: {exc}", flush=True)
        return {
            "category": "general",
            "priority": "medium",
            "department": "customer_success",
            "suggested_response": "Thank you for contacting us. We will review your request and get back to you shortly.",
        }


def format_action_str(action: dict) -> str:
    """Format action for log output."""
    cat = action.get("category", "?")
    pri = action.get("priority", "?")
    dept = action.get("department", "?")
    return f"triage(cat={cat},pri={pri},dept={dept})"


# ── Main inference loop ──────────────────────────────────────────────────────

async def run_task(task_name: str) -> None:
    """Run a single task episode and emit structured logs."""
    from server.triage_environment import SupportTriageEnvironment
    from models import TriageAction

    if IMAGE_NAME:
        env = await SupportTriageEnvironment.from_docker_image(IMAGE_NAME)
    else:
        env = SupportTriageEnvironment(task_name=task_name)

    rewards: List[float] = []
    step_num = 0
    success = False

    log_start(task=task_name, env=ENV_NAME, model=MODEL_NAME)

    try:
<<<<<<< HEAD
        obs = await env.reset(seed=42)
=======
        obs = env.reset(seed=42)
>>>>>>> d8f35e60f36ccd10c0da311a0208ffbe29999d37
        done = obs.done

        while not done and step_num < MAX_STEPS:
            step_num += 1

            # Call LLM to decide triage action
            llm_result = call_llm(
                obs.ticket_subject, obs.ticket_body,
                obs.customer_name, obs.customer_tier,
            )

            # Create typed action
            action = TriageAction(
                category=llm_result.get("category", "general"),
                priority=llm_result.get("priority", "medium"),
                department=llm_result.get("department", "customer_success"),
                suggested_response=llm_result.get("suggested_response", ""),
            )

            # Step the environment
<<<<<<< HEAD
            obs = await env.step(action)
=======
            obs = env.step(action)
>>>>>>> d8f35e60f36ccd10c0da311a0208ffbe29999d37
            reward = obs.reward if obs.reward is not None else 0.0
            done = obs.done
            error = obs.last_action_error

            rewards.append(float(reward))

            log_step(
                step=step_num,
                action=format_action_str(llm_result),
                reward=reward,
                done=done,
                error=error,
            )

        success = True

    except Exception as e:
        step_num += 1
        rewards.append(0.0)
        log_step(step=step_num, action="error()", reward=0.0, done=True, error=str(e))

    finally:
        # Score is the average reward across all tickets, clamped to [0, 1]
        score = sum(rewards) / len(rewards) if rewards else 0.0
        score = max(0.0, min(score, 1.0))
        try:
            await env.close()
        except TypeError:
            # env.close() may not be async in local mode
            try:
                env.close()
            except Exception:
                pass
        except Exception as e:
            print(f"[DEBUG] env.close() error: {e}", flush=True)
        log_end(success=success, steps=step_num, score=score, rewards=rewards)


async def main() -> None:
    """Run inference across all three task difficulties."""
    tasks = ["easy_triage", "medium_triage", "hard_triage"]
    for task_name in tasks:
        await run_task(task_name)
        print()  # Blank line between tasks


if __name__ == "__main__":
    asyncio.run(main())
