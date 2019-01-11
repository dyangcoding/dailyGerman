from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from wtforms.fields.html5 import EmailField

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    subject = StringField('Subject')
    email = EmailField('Email Address', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Send')