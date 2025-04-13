# WhatsApp Daily Reflection Bot

This script sends daily WhatsApp messages using Twilio and saves the responses to a JSON file.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a Twilio account and get your credentials:
   - Sign up at https://www.twilio.com/
   - Get your Account SID and Auth Token
   - Set up a WhatsApp Sandbox for your Twilio number

3. Copy the `.env.example` file to `.env` and fill in your credentials:
```bash
cp .env.example .env
```

4. Edit the `.env` file with your Twilio credentials and phone numbers:
   - `TWILIO_ACCOUNT_SID`: Your Twilio Account SID
   - `TWILIO_AUTH_TOKEN`: Your Twilio Auth Token
   - `TWILIO_PHONE_NUMBER`: Your Twilio phone number (with country code)
   - `RECIPIENT_PHONE_NUMBER`: The recipient's phone number (with country code)

## Usage

Run the script:
```bash
python main.py
```

The script will:
1. Send the first message ("Hi Alon, what was your best moment today?") every day at 21:30 from Sunday to Thursday
2. Wait for the response
3. Send the second message ("Tell me briefly about an inspiration you had today")
4. Save both responses to `responses.json` with the date

## Responses Format

The responses are saved in `responses.json` with the following format:
```json
[
    {
        "date": "YYYY-MM-DD",
        "best_moment": "Response to first question",
        "inspiration": "Response to second question"
    }
]
``` 