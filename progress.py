import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE = os.path.join(BASE_DIR, "user_progress.csv")

if not os.path.exists(FILE):
    with open(FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "levels_completed"])


def get_level(username: str) -> int:
    with open(FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["username"] == username:
                return int(row["levels_completed"])
    return 0


def save_level(username: str, level: int):
    rows = []
    found = False

    with open(FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["username"] == username:
                row["levels_completed"] = level
                found = True
            rows.append(row)

    if not found:
        rows.append({
            "username": username,
            "levels_completed": level
        })

    with open(FILE, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["username", "levels_completed"]
        )
        writer.writeheader()
        writer.writerows(rows)
