from flask_mail import Message
from app import mail
from flask import render_template, current_app
from threading import Thread
import yagmail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def init_yagmail():
    yag = yagmail.SMTP(current_app.config['MAIL_USERNAME'], current_app.config['MAIL_PASSWORD'])
    return yag

def send_mail_yag(subject, msg):
    yag = init_yagmail()
    yag.send(subject, msg)
    
def send_email(subject, sender, recipients, text_body, sync=False):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    if sync:
        mail.send(msg)
    else:
        Thread(target=send_async_email,
                args=(current_app._get_current_object(), msg)).start()