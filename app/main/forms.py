from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, InputRequired, Email

class ContactForm(FlaskForm):
    name = StringField('Name',  [InputRequired("Please enter your name.")])
    subject = StringField('Subject')
    email = StringField("Email",  [InputRequired("Please enter your email address."), Email("This field requires a valid email address")])
    message = TextAreaField('Message', [InputRequired("Not including a message would be stupid")])
    submit = SubmitField('Send')