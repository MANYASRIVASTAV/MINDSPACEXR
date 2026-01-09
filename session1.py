# sessions.py

from state import current_session

# Anxiety level mapping for improvement calculation
_LEVEL_MAP = {
    "high": 3,
    "medium": 2,
    "low": 1
}



def start_session():
    current_session.clear()
    current_session.update({
        "active": True,
        "levels_completed": 0,
        "anxiety_log": [],
        "anxiety_before": None,
        "anxiety_after": None
    })

def log_anxiety(level: str):
    current_session["anxiety_log"].append(level)

    # first input = before
    if current_session["anxiety_before"] is None:
        current_session["anxiety_before"] = level

    # last input = after
    current_session["anxiety_after"] = level

def complete_level():
    current_session["levels_completed"] += 1

def end_session():
    current_session["active"] = False

def calculate_improvement():
    before = _LEVEL_MAP.get(current_session["anxiety_before"], 0)
    after = _LEVEL_MAP.get(current_session["anxiety_after"], 0)

    if before == 0:
        return 0.0

    return round(((before - after) / before) * 100, 2)
