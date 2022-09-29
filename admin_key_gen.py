import os
import smtplib
import random
import datetime
import schedule
import time
from email.message import EmailMessage

EMAIL_ADDRESS = os.getenv('EMAIL_USER')
EMAIL_PASSWORD = os.getenv('EMAIL_PASS')

admin_emails = []
admin_key = str(random.randint(100000, 999999))

date = datetime.datetime.now().strftime('%d %b %Y')

msg = EmailMessage()
msg['Subject'] = f'Daily Password | {date}'
msg['To'] = admin_emails
msg['From'] = EMAIL_ADDRESS
msg.set_content(admin_key)

def send_email():
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
