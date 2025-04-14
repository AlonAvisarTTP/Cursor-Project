import os
import json
from datetime import datetime
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import openai

load_dotenv()

# הגדרות Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials_json = os.getenv("GOOGLE_SHEET_CREDENTIALS_JSON")
creds_dict = json.loads(credentials_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# הגדרות OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# קריאת הגיליון
sheet = client.open("whatsapp_data").sheet1
rows = sheet.get_all_records()

# שליפה רק של תשובות מהיום
today = datetime.now().date()
relevant_rows = []
for row in rows:
    try:
        row_time = datetime.strptime(row["Timestamp"], "%Y-%m-%d %H:%M:%S")
        if row_time.date() == today and row["Answer"]:
            relevant_rows.append(row)
    except:
        continue

# הכנה לפרומפט
answers = [f"Q: {r['Question']}\nA: {r['Answer']}" for r in relevant_rows if r["Question"] and r["Answer"]]
joined = "\n\n".join(answers)

if not joined:
    print("No answers found for today.")
    exit()

prompt = f"""
You are a warm, reflective assistant helping someone summarize their day.  
Based on the following questions and answers, write a short, emotional summary paragraph in English:

{joined}

Start your response with: "This day..."
"""

# בקשת סיכום מ-OpenAI
response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)

summary = response["choices"][0]["message"]["content"]
print("\n📋 Summary for today:\n")
print(summary)
