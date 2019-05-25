from flask_mail import Message
from app import mail
from flask import render_template, current_app
from threading import Thread
from string import Template

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(post_id, sync=False):
    subject = 'Neues Kommentar !'
    recipients = [current_app.config['MAIL_USERNAME']]
    msg = Message(subject, recipients=recipients)
    msg.body = Template('Neues Kommentar www.daily-german.com/post/$id') \
        .substitute(id = post_id)
    if sync:
        mail.send(msg)
    else:
        Thread(target=send_async_email,
                args=(current_app._get_current_object(), msg)).start()