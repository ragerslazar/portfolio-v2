from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Email

class ContactForm(FlaskForm):
    name = StringField("Nom", validators=[DataRequired(message="Ce champs est obligatoire.")])
    prenom = StringField("Prénom", validators=[DataRequired(message="Ce champs est obligatoire.")])
    email = StringField("Email", validators=[DataRequired(message="Ce champs est obligatoire."), Email(message="Veuillez saisir une adresse e-mail valide.")])
    subject = StringField("Sujet", validators=[DataRequired(message="Ce champs est obligatoire.")])
    message = TextAreaField("Message", validators=[DataRequired(message="Ce champs est obligatoire.")])
    submit = SubmitField("Envoyer")