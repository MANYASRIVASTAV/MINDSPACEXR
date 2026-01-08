console.log("script.js loaded");

const API = "http://127.0.0.1:8000";

// ---------- AUTH ----------

async function register() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const res = await fetch(`${API}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });

  const data = await res.json();
  document.getElementById("output").innerText =
    data.message || data.detail;
}

async function login() {
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  const res = await fetch(`${API}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password })
  });

  const data = await res.json();
  document.getElementById("output").innerText =
    data.message || data.detail;

  if (data.message === "login successful") {
    window.location.href = "dashboard.html";
  }
}

if (data.message === "login successful") {
  window.location.href = "dashboard.html";
}


// ---------- SESSION ----------

async function startSession() {
  console.log("Start session");
  await fetch(`${API}/session/start`);
  loadState();
}


async function sendAnxiety(level) {
  console.log("Anxiety:", level);

  await fetch(`${API}/session/anxiety`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ level })
  });

  // ⭐ LOGIC: low anxiety → level cleared
  if (level === "low") {
    await fetch(`${API}/session/level-complete`, {
      method: "POST"
    });
  }

  loadState();
}


async function endSession() {
  console.log("Ending session");

  const res = await fetch(`${API}/session/end`, {
    method: "POST"
  });

  const data = await res.json();
  alert(
    "Session ended\nImprovement: " +
    data.improvement_percent.toFixed(2) + "%"
  );

  loadState();
}


// ---------- STATE ----------

async function loadState() {
  const res = await fetch(`${API}/session/status`);
  const s = await res.json();

  document.getElementById("status").innerText =
    s.active ? "Active" : "Ended";

  document.getElementById("before").innerText =
    s.anxiety_before || "—";

  document.getElementById("after").innerText =
    s.anxiety_after || "—";

  document.getElementById("levels").innerText =
    s.levels_completed;

  const timeline = document.getElementById("timeline");
  timeline.innerHTML = "";

  s.anxiety_log.forEach(a => {
    const span = document.createElement("span");
    span.className = a;
    span.innerText = a.toUpperCase();
    timeline.appendChild(span);
  });
}
