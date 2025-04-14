import os
from flask import Flask, request
from dotenv import load_dotenv
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
from io import StringIO

app = Flask(__name__)
load_dotenv()

@app.route("/", methods=["GET"])
def index():
    return "Bot is up!", 200

@app.route("/whatsapp", methods=["POST"])
def whatsapp():
    incoming_msg = request.form.get('Body')
    sender = request.form.get('From')
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"Received from {sender}: {incoming_msg}")
    
    # שמירה לגיליון עם פונקציה חיצונית
    save_to_google_sheet(now, sender, "", incoming_msg)

    return "OK", 200

def save_to_google_sheet(timestamp, sender, question, answer):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # קריאת האישורים מהסביבה
    credentials_json = os.getenv("GOOGLE_SHEET_CREDENTIALS_JSON")
    creds_dict = json.loads(credentials_json)
    creds_file = StringIO(json.dumps(creds_dict))
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)

    sheet = client.open("whatsapp_data").sheet1
    sheet.append_row([timestamp, sender, question, answer])