import os
import json
from datetime import datetime
from dotenv import load_dotenv
from twilio.rest import Client
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

# Load environment variables
load_dotenv()

# Twilio credentials
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
recipient_phone_number = os.getenv('RECIPIENT_PHONE_NUMBER')

# Initialize Twilio client
client = Client(account_sid, auth_token)

# File to store responses
RESPONSES_FILE = 'responses.json'

def load_responses():
    if os.path.exists(RESPONSES_FILE):
        with open(RESPONSES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_responses(responses):
    with open(RESPONSES_FILE, 'w') as f:
        json.dump(responses, f, indent=4)

def send_first_message():
    message = client.messages.create(
        body="Hi Alon, what was your best moment today?",
        from_=f'whatsapp:{twilio_phone_number}',
        to=f'whatsapp:{recipient_phone_number}'
    )
    print(f"First message sent: {message.sid}")

def send_second_message():
    message = client.messages.create(
        body="Tell me briefly about an inspiration you had today",
        from_=f'whatsapp:{twilio_phone_number}',
        to=f'whatsapp:{recipient_phone_number}'
    )
    print(f"Second message sent: {message.sid}")

def handle_incoming_message(message):
    responses = load_responses()
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Check if we have responses for today
    today_responses = next((r for r in responses if r['date'] == today), None)
    
    if not today_responses:
        today_responses = {
            'date': today,
            'best_moment': None,
            'inspiration': None
        }
        responses.append(today_responses)
    
    # Update the appropriate response based on which question was asked
    if today_responses['best_moment'] is None:
        today_responses['best_moment'] = message.body
        save_responses(responses)
        send_second_message()
    elif today_responses['inspiration'] is None:
        today_responses['inspiration'] = message.body
        save_responses(responses)

def main():
    # Create scheduler
    scheduler = BlockingScheduler()
    
    # Schedule the first message from Sunday to Thursday at 21:30
    scheduler.add_job(
        send_first_message,
        CronTrigger(
            day_of_week='0-4',  # Sunday to Thursday
            hour=21,
            minute=30
        )
    )
    
    print("Scheduler started. Press Ctrl+C to exit.")
    scheduler.start()

if __name__ == "__main__":
    main()


