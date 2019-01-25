from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Email

class ContactForm(FlaskForm):
    name = StringField('Name',  [InputRequired("Bitte deinen Name angeben.")])
    subject = StringField('Betreff')
    email = StringField("Email",  [InputRequired("Bitte Email Adresse angeben."), \
             Email("Dieses Feld erfordert eine gültige EMail Adresse")])
    message = TextAreaField('Nachricht', [InputRequired("Eine leere Nachricht \
                ist doch doof oder ?")])
    submit = SubmitField('Senden')

class CommentForm(FlaskForm):
    name = StringField('Name',  [InputRequired("Bitte deinen Name angeben.")])
    comment = TextAreaField('Kommentar', [InputRequired("Ein Kommentar \
                ist erforderlich. ")])
    recaptcha = RecaptchaField()
    submit = SubmitField('Senden')