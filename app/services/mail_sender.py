import asyncio
from email.message import EmailMessage
from fastapi import Form
import ssl
import smtplib
from config.django.base import EMAIL_PASSWORD, EMAIL_SENDER


def send_single_email(recipient: str, subject: str, body: str):

    msg = EmailMessage()
    msg.set_content(body)
    msg["From"] = EMAIL_SENDER
    msg["To"] = recipient
    msg["Subject"] = subject

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)

        print("Successful sent email to new user")

