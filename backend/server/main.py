from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from twilio.rest import Client
from datetime import datetime
import os
import re

from func import (
    load_users, save_users,
    load_alerts, save_alerts,
    get_sms_text, VALID_DEVICE_IDS
)

# for loading ngrok (reverse proxy) configuration on miko laptop
import ngrok
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
CORS(app)

VALID_PRESS_COUNTS = {1, 2, 3}
PHONE_RE = re.compile(r"^\+?[1-9]\d{6,14}$")


# ── helpers ───────────────────────────────────────────────────────────────────

def _require_json(*fields):
    data = request.get_json(silent=True) or {}
    missing = [f for f in fields if not data.get(f)]
    if missing:
        abort(400, description=f"Missing fields: {', '.join(missing)}")
    return data


def _send_sms(to_number, body):
    sid      = os.environ.get("TWILIO_SID")
    token    = os.environ.get("TWILIO_TOKEN")
    from_num = os.environ.get("TWILIO_NUM")

    if not (sid and token and from_num):
        print("[SMS skipped] would send:\n", body)
        return "skipped"

    try:
        Client(sid, token).messages.create(body=body, from_=from_num, to=to_number)
        return "sent"
    except Exception as e:
        print("[Twilio error]", e)
        return "failed"


# ── routes ────────────────────────────────────────────────────────────────────

@app.route("/register", methods=["POST"])
def register():
    data = _require_json("device_id", "name", "email", "password")

    device_id = data["device_id"]

    # only known device IDs can register
    if device_id not in VALID_DEVICE_IDS:
        return jsonify({"error": "Device ID not recognised. Check the ID printed on your device."}), 400

    users = load_users()

    if device_id in users:
        return jsonify({"error": "Device already registered. Please sign in."}), 400

    contacts_raw = data.get("contacts", {})
    contacts = {}
    for key in ("1", "2", "3"):
        contact = contacts_raw.get(key)
        if not isinstance(contact, dict) or not contact.get("name") or not contact.get("phone"):
            abort(400, description=f"Contact {key} needs 'name' and 'phone'.")
        if not PHONE_RE.match(contact["phone"]):
            abort(400, description=f"Contact {key} phone number looks invalid. Use international format e.g. +447700000000")
        contacts[key] = {"name": contact["name"], "phone": contact["phone"]}

    users[device_id] = {
        "device_id":     device_id,
        "name":          data["name"],
        "email":         data["email"],
        "password":      data["password"],
        "medical_notes": data.get("medical_notes", ""),
        "contacts":      contacts,
        "registered_at": datetime.now().isoformat(),
    }
    save_users(users)

    return jsonify({"status": "registered", "device_id": device_id}), 201


@app.route("/login", methods=["POST"])
def login():
    data = _require_json("device_id", "password")

    users = load_users()
    user  = users.get(data["device_id"])

    if not user:
        return jsonify({"error": "Device not found. Check your ID or register first."}), 404

    if user["password"] != data["password"]:
        return jsonify({"error": "Incorrect password."}), 401

    return jsonify({
        "status":    "ok",
        "device_id": user["device_id"],
        "name":      user["name"],
        "email":     user["email"],
    }), 200


@app.route("/alert", methods=["POST"])
def alert():
    data = _require_json("device_id", "press_count", "lat", "lon")

    press_count = data["press_count"]
    if press_count not in VALID_PRESS_COUNTS:
        abort(400, description="press_count must be 1, 2, or 3.")

    try:
        lat, lon = float(data["lat"]), float(data["lon"])
    except (TypeError, ValueError):
        abort(400, description="lat and lon must be numbers.")

    users = load_users()
    if data["device_id"] not in users:
        abort(404, description="Device not registered.")

    user    = users[data["device_id"]]
    contact = user["contacts"][str(press_count)]

    sms_text   = get_sms_text(user, press_count, lat, lon)
    sms_status = _send_sms(contact["phone"], sms_text)

    alerts = load_alerts()
    alerts.append({
        "device_id":     data["device_id"],
        "user_name":     user["name"],
        "press_count":   press_count,
        "contact_name":  contact["name"],
        "contact_phone": contact["phone"],
        "lat":           lat,
        "lon":           lon,
        "time":          datetime.now().isoformat(),
        "sms_status":    sms_status,
    })
    save_alerts(alerts)

    return jsonify({
        "status":  "alert sent",
        "contact": contact["name"],
        "sms":     sms_status,
    }), 200


@app.route("/alerts", methods=["GET"])
def get_alerts():
    alerts = list(reversed(load_alerts()))
    try:
        page     = max(1, int(request.args.get("page", 1)))
        per_page = min(200, max(1, int(request.args.get("per_page", 50))))
    except ValueError:
        abort(400, description="page and per_page must be integers.")
    start = (page - 1) * per_page
    return jsonify({
        "total":    len(alerts),
        "page":     page,
        "per_page": per_page,
        "alerts":   alerts[start:start + per_page],
    }), 200


@app.route("/user/<device_id>", methods=["GET"])
def get_user(device_id):
    users = load_users()
    if device_id not in users:
        abort(404, description="User not found.")
    user = users[device_id]
    return jsonify({
        "name":          user["name"],
        "email":         user.get("email", ""),
        "device_id":     user["device_id"],
        "registered_at": user["registered_at"],
    }), 200


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok"}), 200


@app.errorhandler(400)
@app.errorhandler(401)
@app.errorhandler(404)
def http_error(e):
    return jsonify({"error": e.description}), e.code




# ------- NGROK DO NOT TOUCH ----------

# Connects to ngrok directly
def connect_ngrok():
    forwarder = ngrok.forward("localhost:5000", authtoken_from_env=True)
    print(f"Available at: {forwarder.url()}")
    import subprocess
    #subprocess.run .split(" ")
    subprocess.call(f"""./transferToPi.sh -s {forwarder.url()}""".split(" "))


# Tries to execute above function
try:
    connect_ngrok()
except Exception as e:
    print("Not on miko laptop. Connecting to ngrok wont work")
    print(e)
