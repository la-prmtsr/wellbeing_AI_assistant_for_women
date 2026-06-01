from agent.memory import load_data


def get_last_n_entries(n=7):
    """
    Son n kaydı döndürür.
    """
    data = load_data()
    return data[-n:] if data else []


def calculate_summary(entries):
    """
    Ortalama mood, stress ve sleep değerlerini hesaplar.
    """
    if not entries:
        return {
            "avg_mood": 0,
            "avg_stress": 0,
            "avg_sleep": 0
        }

    total_mood = sum(entry.get("mood", 0) for entry in entries)
    total_stress = sum(entry.get("stress", 0) for entry in entries)
    total_sleep = sum(entry.get("sleep", 0) for entry in entries)

    count = len(entries)

    return {
        "avg_mood": round(total_mood / count, 1),
        "avg_stress": round(total_stress / count, 1),
        "avg_sleep": round(total_sleep / count, 1)
    }


def compare_with_previous(entries):
    """
    Son kayıt ile bir önceki kaydı karşılaştırır.
    """
    if len(entries) < 2:
        return {
            "mood_change": 0,
            "stress_change": 0,
            "sleep_change": 0
        }

    current = entries[-1]
    previous = entries[-2]

    return {
        "mood_change": current.get("mood", 0) - previous.get("mood", 0),
        "stress_change": current.get("stress", 0) - previous.get("stress", 0),
        "sleep_change": current.get("sleep", 0) - previous.get("sleep", 0)
    }