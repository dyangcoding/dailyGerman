from flask_mail import Message
from app import mail
from flask import render_template, current_app
from threading import Thread
import smtplib, ssl

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def smtp_ssl_send():
    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:          
        server.login(sender_email, password)
        msg = message2Html('test html sending', html)
        server.sendmail(sender_email, receiver_email, msg.as_string())

def send_email(subject, sender, recipients, text_body, sync=False):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    if sync:
        mail.send(msg)
    else:
        Thread(target=send_async_email,
                args=(current_app._get_current_object(), msg)).start()