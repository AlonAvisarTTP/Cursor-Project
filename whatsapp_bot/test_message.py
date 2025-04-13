import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

from_whatsapp = os.getenv("TWILIO_PHONE_NUMBER")
to_whatsapp = os.getenv("RECIPIENT_PHONE_NUMBER")

message = client.messages.create(
    from_=from_whatsapp,
    body="Hi Alon, what was your best moment today?",
    to=to_whatsapp
)

print(f"Message sent! SID: {message.sid}")
