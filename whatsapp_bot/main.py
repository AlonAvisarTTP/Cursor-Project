import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
client.messages.create(
    from_=os.getenv("TWILIO_PHONE_NUMBER"),
    to=os.getenv("RECIPIENT_PHONE_NUMBER"),
    body="Hi Alon, what was your best moment today?"
)
print("✅ Sent: first question")
