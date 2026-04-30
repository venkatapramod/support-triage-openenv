#!/usr/bin/env python3
"""
Pre-submission validation script.
Checks all requirements before submitting to the hackathon.
"""

import os
import sys
import json
import importlib

PASS = "✅ PASS"
FAIL = "❌ FAIL"
results = []


def check(name, condition, detail=""):
    status = PASS if condition else FAIL
    results.append((name, condition))
    msg = f"{status}: {name}"
    if detail:
        msg += f" — {detail}"
    print(msg)
    return condition


print("=" * 60)
print("  OpenEnv Hackathon Pre-Submission Validator")
print("=" * 60)
print()


print("--- File Structure ---")
check("inference.py exists in root", os.path.isfile("inference.py"))
check("models.py exists", os.path.isfile("models.py"))
check("tickets.py exists", os.path.isfile("tickets.py"))
check("openenv.yaml exists", os.path.isfile("openenv.yaml"))
check("Dockerfile exists", os.path.isfile("Dockerfile"))
check("README.md exists", os.path.isfile("README.md"))
check("server/app.py exists", os.path.isfile("server/app.py"))
check("server/triage_environment.py exists", os.path.isfile("server/triage_environment.py"))
check("server/requirements.txt exists", os.path.isfile("server/requirements.txt"))
print()


print("--- inference.py Checks ---")
with open("inference.py", "r") as f:
    inf_content = f.read()

check("Uses 'from openai import OpenAI'", "from openai import OpenAI" in inf_content)
check("Reads API_BASE_URL with default", 'os.getenv("API_BASE_URL"' in inf_content and "https://" in inf_content)
check("Reads MODEL_NAME with default", 'os.getenv("MODEL_NAME"' in inf_content)
check("Reads HF_TOKEN without default", 'os.getenv("HF_TOKEN")' in inf_content)
check("HF_TOKEN has no default value",
      'os.getenv("HF_TOKEN")' in inf_content and 'os.getenv("HF_TOKEN",)' not in inf_content)
check("Raises error if HF_TOKEN missing", "HF_TOKEN is None" in inf_content or "not HF_TOKEN" in inf_content)
check("Has [START] log format", "[START]" in inf_content)
check("Has [STEP] log format", "[STEP]" in inf_content)
check("Has [END] log format", "[END]" in inf_content)
print()


print("--- Environment Tests ---")
try:
    from server.triage_environment import SupportTriageEnvironment
    from models import TriageAction
    check("Environment imports successfully", True)
except Exception as e:
    check("Environment imports successfully", False, str(e))
    print("\nCannot continue without environment imports.")
    sys.exit(1)


for task_name in ["easy_triage", "medium_triage", "hard_triage"]:
    try:
        env = SupportTriageEnvironment(task_name=task_name)
        obs = env.reset(seed=42)
        check(f"{task_name}: reset() works", obs is not None)
        check(f"{task_name}: reset returns observation with ticket",
              hasattr(obs, "ticket_subject") and len(obs.ticket_subject) > 0)

        steps = 0
        all_rewards_valid = True
        while not obs.done:
            action = TriageAction(
                category="billing", priority="high",
                department="finance",
                suggested_response="We will look into this."
            )
            obs = env.step(action)
            steps += 1
            r = obs.reward if obs.reward is not None else 0.0
            if not (0.0 <= r <= 1.0):
                all_rewards_valid = False

        state = env.state
        check(f"{task_name}: completes without error", True)
        check(f"{task_name}: rewards in [0.0, 1.0]", all_rewards_valid)
        check(f"{task_name}: state has episode_id", state.episode_id is not None)
        check(f"{task_name}: state has step_count", state.step_count == steps)

    except Exception as e:
        check(f"{task_name}: runs successfully", False, str(e))

print()


print("--- Grader Quality Checks ---")
env = SupportTriageEnvironment(task_name="easy_triage")
obs = env.reset(seed=42)


action_correct = TriageAction(
    category="billing", priority="high", department="finance",
    suggested_response="We will process your refund for the duplicate charge immediately."
)
obs_correct = env.step(action_correct)

env2 = SupportTriageEnvironment(task_name="easy_triage")
obs2 = env2.reset(seed=42)


action_wrong = TriageAction(
    category="shipping", priority="low", department="engineering",
    suggested_response="test"
)
obs_wrong = env2.step(action_wrong)

r_correct = obs_correct.reward if obs_correct.reward else 0
r_wrong = obs_wrong.reward if obs_wrong.reward else 0

check("Correct action gets higher reward than wrong action",
      r_correct > r_wrong,
      f"correct={r_correct:.2f}, wrong={r_wrong:.2f}")
check("Wrong action still gets some reward (partial credit exists)",
      r_wrong >= 0.0)
check("Reward difference is meaningful",
      r_correct - r_wrong >= 0.3,
      f"difference={r_correct - r_wrong:.2f}")
print()

#  Check FastAPI app
print("--- Server Checks ---")
try:
    os.environ["TRIAGE_TASK"] = "easy_triage"
    from fastapi.testclient import TestClient
    from server.app import app

    tc = TestClient(app)

    r = tc.get("/health")
    check("GET /health returns 200", r.status_code == 200)

    r = tc.post("/reset", json={})
    check("POST /reset returns 200", r.status_code == 200)
    check("Reset response has observation", "observation" in r.json())

    r = tc.get("/state")
    check("GET /state returns 200", r.status_code == 200)

    r = tc.get("/schema")
    check("GET /schema returns 200", r.status_code == 200)

except Exception as e:
    check("FastAPI server works", False, str(e))

print()


print("--- openenv.yaml Checks ---")
try:
    import yaml
    with open("openenv.yaml", "r") as f:
        config = yaml.safe_load(f)
    check("openenv.yaml is valid YAML", True)
    check("Has name field", "name" in config)
    check("Has version field", "version" in config)
    check("Has description", "description" in config)
    check("Has tasks list", "tasks" in config and len(config["tasks"]) >= 3)
    check("Has action_space", "action_space" in config)
    check("Has observation_space", "observation_space" in config)
    check("Has reward_range", "reward_range" in config)
except ImportError:
    print("⚠️  PyYAML not installed, skipping YAML validation")
except Exception as e:
    check("openenv.yaml is valid", False, str(e))

print()


print("=" * 60)
passed = sum(1 for _, ok in results if ok)
total = len(results)
failed = total - passed
print(f"  Results: {passed}/{total} passed, {failed} failed")
if failed == 0:
    print("  🎉 ALL CHECKS PASSED — Ready to submit!")
else:
    print("  ⚠️  Some checks failed — review above")
print("=" * 60)
