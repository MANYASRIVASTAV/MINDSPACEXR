# app.py
from fastapi.middleware.cors import CORSMiddleware

import csv
import os
from fastapi import HTTPException
from pydantic import BaseModel
from fastapi import FastAPI
from models import AnxietyInput
from sessions import (
    start_session,
    log_anxiety,
    complete_level,
    end_session,
    calculate_improvement
)
from state import current_session

app = FastAPI(title="Phobia VR Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "backend alive"}

@app.get("/session/start")
def session_start():
    start_session()
    return {
        "message": "session started",
        "session": current_session
    }

@app.post("/session/anxiety")
def receive_anxiety(data: AnxietyInput):
    log_anxiety(data.level)
    return {
        "message": "anxiety logged",
        "current_level": data.level
    }

@app.post("/session/level-complete")
def level_complete():
    complete_level()
    return {
        "message": "level completed",
        "levels_completed": current_session["levels_completed"]
    }

@app.post("/session/end")
def session_end():
    end_session()
    improvement = calculate_improvement()
    return {
        "message": "session ended",
        "improvement_percent": improvement
    }

@app.get("/session/status")
def session_status():
    return current_session


USERS_FILE = "users.csv"

class UserAuth(BaseModel):
    username: str
    password: str

# ensure csv exists
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["username", "password"])

@app.post("/auth/register")
def register(user: UserAuth):
    with open(USERS_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["username"] == user.username:
                raise HTTPException(status_code=400, detail="User already exists")

    with open(USERS_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([user.username, user.password])

    return {"message": "registered successfully"}

@app.post("/auth/login")
def login(user: UserAuth):
    with open(USERS_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["username"] == user.username and row["password"] == user.password:
                return {"message": "login successful"}

    raise HTTPException(status_code=401, detail="invalid credentials")



