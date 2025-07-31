from flask import Flask, render_template, request
from flask_mail import Mail, Message
import logging
import os

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.mail.yahoo.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


@app.route('/', methods=["GET", "POST"])
def home():
    user_agent: str = request.headers.get("User-Agent")
    icon_per_line: int = 6 if "Mobile" in user_agent else 9
    email_sent: bool = None

    if request.method == "POST" and request.form["email"] != "":
        try:
            name: str = request.form["name"]
            prenom: str = request.form["prenom"]
            email: str = request.form["email"]
            subject: str = request.form["subject"]
            message: str = request.form["message"]

            msg = Message("📨 Nouveau message [Portfolio]",
                          sender=app.config['MAIL_USERNAME'],
                          recipients=[app.config['MAIL_USERNAME']])
            msg.body = f"""
            📨 Nouveau message reçu depuis ton portfolio
    
            👤 Informations du visiteur :
            - Nom : {name}
            - Prénom : {prenom}
            - Email : {email}
            - Sujet : {subject}
    
            📝 Message :
            {message}
            """

            mail.send(msg)
            email_sent = True
            logging.info("Mail envoyé avec succès !")
        except Exception as e:
            email_sent = False
            logging.error(f"Mail error: {e}")
    elif request.method == "GET":
        pass
    else:
        email_sent = False
        logging.error("Mail error")

    return render_template('index.html', icon_per_line = icon_per_line, email_sent = email_sent)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")