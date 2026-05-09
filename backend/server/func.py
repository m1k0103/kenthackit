import json
import os
import threading
from datetime import datetime

USERS_FILE = "data/users.json"
ALERTS_FILE = "data/alerts.json"

_lock = threading.Lock()


def _ensure_dir(filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with _lock, open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    _ensure_dir(USERS_FILE)
    with _lock, open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)


def load_alerts():
    if not os.path.exists(ALERTS_FILE):
        return []
    with _lock, open(ALERTS_FILE, "r") as f:
        return json.load(f)


def save_alerts(alerts):
    _ensure_dir(ALERTS_FILE)
    with _lock, open(ALERTS_FILE, "w") as f:
        json.dump(alerts, f, indent=2)


def get_maps_link(lat, lon):
    return f"https://maps.google.com/?q={lat},{lon}"


def get_sms_text(user, press_count, lat, lon):
    link = get_maps_link(lat, lon)
    time_now = datetime.now().strftime("%H:%M, %d %b %Y")

    if press_count == 1:
        msg = "FAMILY ALERT\n"
    elif press_count == 2:
        msg = "POLICE NEEDED\n"
    else:
        msg = "MEDICAL EMERGENCY\n"

    msg += f"From: {user['name']}\n"
    msg += f"Location: {link}\n"
    msg += f"Time: {time_now}"

    medical = (user.get("medical_notes") or "").strip()
    if press_count == 3 and medical:
        msg += f"\nMedical info: {medical}"

    return msg