import json
import os

FILE_PATH = "data/profiles.json"


def load_profiles():
    if not os.path.exists(FILE_PATH):
        return {}

    try:
        with open(FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_profiles(profiles):
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(profiles, f, indent=4, ensure_ascii=False, default=str)


def save_user_profile(username, period_dates, cycle_info):
    profiles = load_profiles()

    profiles[username] = {
        "period_dates": period_dates,
        "cycle_info": cycle_info
    }

    save_profiles(profiles)


def load_user_profile(username):
    profiles = load_profiles()
    return profiles.get(username)


def username_exists(username):
    profiles = load_profiles()
    return username in profiles