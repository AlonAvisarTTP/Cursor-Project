import os
import json
from datetime import datetime
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import openai
from twilio.rest import Client

load_dotenv()

# הגדרות Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
credentials_json = os.getenv("GOOGLE_SHEET_CREDENTIALS_JSON")
creds_dict = json.loads(credentials_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client_gs = gspread.authorize(creds)

# הגדרות OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# קריאת הגיליון
sheet = client_gs.open("whatsapp_data").sheet1
rows = sheet.get_all_records()

# שליפה רק של תשובות מהיום
today = datetime.now()
start_of_week = today - timedelta(days=today.weekday())  # יום ראשון
end_of_week = start_of_week + timedelta(days=4)          # יום חמישי

relevant_rows = []
for row in rows:
    try:
        row_time = datetime.strptime(row["Timestamp"], "%Y-%m-%d %H:%M:%S")
        if start_of_week.date() <= row_time.date() <= end_of_week.date() and row["Answer"]:
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
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}]
)

summary = response["choices"][0]["message"]["content"]

# עיצוב – ירידת שורה אחרי כל נקודה
formatted_summary = summary.replace(". ", ".\n")
summary_intro = "🗓️ Here's your weekly reflection summary:\n\n"
final_message = summary_intro + formatted_summary

# הדפסה למסך
print("\n📋 Summary for your week:\n")
print(final_message)

# שליחה לוואטסאפ
client_twilio = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
client_twilio.messages.create(
    from_=os.getenv("TWILIO_PHONE_NUMBER"),
    to=os.getenv("RECIPIENT_PHONE_NUMBER"),
    body="📋 ummary for your week:\n\n" + final_message
)

print("✅ Summary sent via WhatsApp!")
print("🧠 Weekly summary ran on schedule.")

 