from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from wtforms.fields.html5 import EmailField

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    subject = StringField('Subject')
    email = EmailField('Email Address', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Send')

class CommentForm(FlaskForm):
    author = StringField('Name', validators=[DataRequired()])
    comment = TextAreaField('Kommentar', validators=[DataRequired('Ein Kommentar \
                ist erforderlich. ')])
    recaptcha = RecaptchaField()
    submit = SubmitField('Senden')