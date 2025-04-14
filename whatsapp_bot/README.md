# 📱 WhatsApp Daily Reflection Bot

An AI-powered WhatsApp bot that asks you reflective questions each evening and sends you a beautiful weekly summary every Friday.

## ✨ Features

- 📅 Sends you a daily question every evening at 21:30
- 💬 Handles your answers in natural conversation flow
- 📊 Saves all data to Google Sheets
- 🧠 Uses OpenAI to generate emotional weekly summaries
- 💌 Sends the summary back to you via WhatsApp every Friday at 16:00

## 🛠 Tech Stack

- Python
- Twilio (WhatsApp API)
- OpenAI (GPT-3.5)
- Google Sheets (via `gspread`)
- GitHub Actions (for scheduling)

## 🔄 How It Works

1. Every day at 21:30:
   - Bot sends: “Hi Alon, what was your best moment today?”
   - After reply: “Tell me briefly about an inspiration you had today”
2. All answers are stored in a Google Sheet
3. Every Friday at 16:00:
   - The bot collects all answers from Sunday to Thursday
   - It generates a short emotional summary using GPT
   - Sends it to you on WhatsApp

## 🔐 Environment Variables

Set these as GitHub Actions secrets:

- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER`
- `RECIPIENT_PHONE_NUMBER`
- `OPENAI_API_KEY`
- `GOOGLE_SHEET_CREDENTIALS_JSON`


## ✅ Setup Status

- [x] Fully deployed in the cloud
- [x] Zero-cost using GitHub Actions
- [x] Sends and receives messages
- [x] Summarizes using GPT
- [x] Logs to Google Sheets

Built by Alon Avisar ❤️
