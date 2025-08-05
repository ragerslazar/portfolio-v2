from logging import Logger
from typing import Optional

from flask import Flask, Request
from flask_mail import Mail, Message


class Mailer:
    def __init__(self, request: Request, mail_app: Mail, app: Flask, logging: Logger):
        self.request: Request = request
        self.name: Optional[str] = self.request.form.get("name") or None
        self.prenom: Optional[str] = self.request.form.get("prenom") or None
        self.email: Optional[str] = self.request.form.get("email") or None
        self.subject: Optional[str] = self.request.form.get("subject") or None
        self.message: Optional[str] = self.request.form.get("message") or None
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