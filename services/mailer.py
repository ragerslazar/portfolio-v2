from logging import Logger
from typing import Optional
from flask import Flask
from flask_mail import Mail, Message
from forms.ContactForm import ContactForm

class Mailer:
    def __init__(self, form: ContactForm, mail_app: Mail, app: Flask, logging: Logger):
        self.form: ContactForm = form
        self.name: Optional[str] = self.form.name.data
        self.prenom: Optional[str] = self.form.prenom.data
        self.email: Optional[str] = self.form.email.data
        self.subject: Optional[str] = self.form.subject.data
        self.message: Optional[str] = self.form.message.data
        self.mail: Mail = mail_app
        self.app: Flask = app
        self.logging: Logger = logging
        self.sent: Optional[bool] = None


    def sendMail(self)-> bool:
        try:
            msg = Message("📨 Nouveau message [Portfolio]",
                          sender=self.app.config['MAIL_USERNAME'],
                          recipients=[self.app.config['MAIL_USERNAME']])
            msg.body = \
            f"""📨 Nouveau message reçu depuis ton portfolio
            👤 Informations du visiteur :
            - Nom : {self.name}
            - Prénom : {self.prenom}
            - Email : {self.email}
            - Sujet : {self.subject}

            📝 Message :
            {self.message}
            """

            self.mail.send(msg)
            self.sent = True
            self.logging.info("Mail envoyé avec succès !")
        except Exception as e:
            self.sent = False
            self.logging.error(f"Mail error: {e}")

        return self.sent