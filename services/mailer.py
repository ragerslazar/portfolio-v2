from flask import Flask, Request
from flask_mail import Mail, Message


class Mailer:
    def __init__(self, request: Request, mail_app: Mail, app: Flask, logging):
        self.request = request
        self.name = self.request.form["name"]
        self.prenom = self.request.form["prenom"]
        self.email = self.request.form["email"]
        self.subject = self.request.form["subject"]
        self.message = self.request.form["message"]
        self.mail = mail_app
        self.app = app
        self.logging = logging
        self.sent = None


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