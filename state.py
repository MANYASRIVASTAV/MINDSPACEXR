# state.py

current_session = {
    "active": False,          # session running or not
    "levels_completed": 0,    # how many stages cleared
    "anxiety_log": [],        # list of anxiety inputs over time
    "anxiety_before": None,   # first anxiety level
    "anxiety_after": None     # last anxiety level
}
