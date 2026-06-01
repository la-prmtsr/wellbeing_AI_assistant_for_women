import json
import os
from datetime import datetime

FILE_PATH = "data/user_data.json"

def load_data():
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, "r") as f:
        return json.load(f)

def save_data(entry):
    data = load_data()
    data.append(entry)
    with open(FILE_PATH, "w") as f:
        json.dump(data, f, indent=4)

def get_recent_history(limit=5):
    data = load_data()
    return data[-limit:] if data else []

def create_entry(mood, stress, sleep, cycle_day, note):
    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "mood": mood,
        "stress": stress,
        "sleep": sleep,
        "cycle_day": cycle_day,
        "note": note
    }