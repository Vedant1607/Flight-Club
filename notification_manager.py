import os
from dotenv import load_dotenv
from twilio.rest import Client
class NotificationManager:
    def __init__(self):
        load_dotenv()
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.client = Client(self.account_sid,self.auth_token)
        self.twilio_from = os.getenv('TWILIO_PHONE_NUMBER')
        self.twilio_to = os.getenv('TWILIO_TO')
    
    def send_sms(self,message_body):
        # Method to send sms
        message = self.client.messages.create(
            body=message_body,
            from_= self.twilio_from,
            to=self.twilio_to
        )
        print(message.sid)
    
    def send_wp_message(self,message_body):
        # Method to senf message on whatsapp
        message = self.client.messages.create(
            body=message_body,
            from_='whatsapp:+14155238886' f"whatsapp:{os.getenv('TWILIO_WP_NUMBER')}",
            to=f'whatsapp:{self.twilio_to}'
        )
        print(message.sid)