import os
from flask import Flask, request
from dotenv import load_dotenv
from datetime import datetime
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from twilio.rest import Client

app = Flask(__name__)
load_dotenv()

conversation_state = {}

def send_whatsapp_message(to, message):
    client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
    client.messages.create(
        from_=os.getenv("TWILIO_PHONE_NUMBER"),
        to=to,
        body=message
    )

def save_to_google_sheet(timestamp, sender, question, answer):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(os.getenv("GOOGLE_SHEET_CREDENTIALS_JSON")), scope)
    client = gspread.authorize(creds)
    sheet = client.open("whatsapp_data").sheet1
    sheet.append_row([timestamp, sender, question, answer])

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.form.get('Body')
    sender = request.form.get('From')
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"Received from {sender}: {incoming_msg}")
    state = conversation_state.get(sender)

    if state == "waiting_for_inspiration":
        save_to_google_sheet(now, sender, "Inspiration of the day", incoming_msg)
        conversation_state[sender] = None
    else:
        save_to_google_sheet(now, sender, "Best moment of the day", incoming_msg)
        send_whatsapp_message(sender, "Tell me briefly about an inspiration you had today")
        conversation_state[sender] = "waiting_for_inspiration"

    return "OK", 200
