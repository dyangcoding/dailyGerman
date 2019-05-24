from flask_mail import Message
from app import mail
from flask import render_template, current_app
from threading import Thread
from string import Template

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)
    
def send_email(user_name, post_name, sync=False):
    subject = 'Neues Kommentar !'
    recipients = [current_app.config['MAIL_USERNAME']]
    msg = Message(subject, recipients=recipients)
    msg.body = Template('$name postet ein Kommentar bei Post $post') \
        .substitute(name = user_name, post = post_name)
    if sync:
        mail.send(msg)
    else:
        Thread(target=send_async_email,
                args=(current_app._get_current_object(), msg)).start()