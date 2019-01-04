from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField

class ContactForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    subject = StringField('subject')
    email = EmailField('Email Address', validators=[DataRequired()])
    message = TextAreaField('message', validators=[DataRequired()])
    submit = SubmitField('Send')