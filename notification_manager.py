import os
from dotenv import load_dotenv
from twilio.rest import Client
import smtplib
class NotificationManager:
    def __init__(self):
        load_dotenv()
        # Twilio API keys for SMS and WhatsApp
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.client = Client(self.account_sid,self.auth_token)
        self.twilio_from = os.getenv('TWILIO_PHONE_NUMBER')
        self.twilio_to = os.getenv('TWILIO_TO')
        
        # Email configurations
        self.smtp_address = os.getenv('EMAIL_PROVIDER_SMTP_ADDRESS')
        self.email = os.getenv('MY_EMAIL')
        self.email_password = os.getenv('MY_EMAIL_PASSWORD')
        self.connection = smtplib.SMTP(self.smtp_address,port=587)
    
    def send_sms(self,message_body):
        # Method to send sms
        message = self.client.messages.create(
            body=message_body,
            from_= self.twilio_from,
            to=self.twilio_to
        )
    
    def send_wp_message(self,message_body):
        # Method to senf message on whatsapp
        message = self.client.messages.create(
            body=message_body,
            from_=f"whatsapp:{os.getenv('TWILIO_WP_NUMBER')}",
            to=f'whatsapp:{self.twilio_to}'
        )
    
    # Function to send an email to a list of recipients
    def send_email(self,email_list,email_body):
        with self.connection:
            self.connection.starttls()
            self.connection.login(user=self.email,password=self.email_password)
            for email in email_list:
                self.connection.sendmail(
                    from_addr=self.email,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{email_body}".encode('utf-8')
                )