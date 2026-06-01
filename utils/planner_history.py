import json
import os
from datetime import datetime

FILE_PATH = "data/planner_history.json"


def load_plans():
    if not os.path.exists(FILE_PATH):
        return []

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_plan(username, goal, plan):
    plans = load_plans()

    plans.append({
        "username": username,
        "goal": goal,
        "plan": plan,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(plans, f, indent=4, ensure_ascii=False)


def get_recent_plans(username, limit=3):
    plans = load_plans()

    user_plans = [
        p for p in plans
        if p.get("username") == username
    ]

    return list(reversed(user_plans[-limit:]))