import os
from flask import Flask, request
from dotenv import load_dotenv
from datetime import datetime
import json

app = Flask(__name__)
load_dotenv()

RESPONSES_FILE = "data/answers.json"

@app.route("/", methods=["GET"])
def index():
    return "Bot is up!", 200

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.form.get('Body')
    sender = request.form.get('From')

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = {"timestamp": now, "sender": sender, "message": incoming_msg}

    os.makedirs("data", exist_ok=True)

    if not os.path.exists(RESPONSES_FILE):
        with open(RESPONSES_FILE, "w") as f:
            json.dump([], f)

    with open(RESPONSES_FILE, "r+") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []
        data.append(entry)
        f.seek(0)
        json.dump(data, f, indent=2)

    return "OK", 200
