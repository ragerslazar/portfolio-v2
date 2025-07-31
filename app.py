from typing import Optional

from flask import Flask, render_template, request
from flask_mail import Mail
import logging
import os
from services.mailer import Mailer

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
    email_sent: Optional[bool] = None

    if request.method == "POST" and request.form["email"] != "":
        mailer = Mailer(request, mail, app, logging)
        email_sent = mailer.sendMail()
    elif request.method == "GET":
        pass
    else:
        email_sent = False
        logging.error("Mail error")

    return render_template('index.html', icon_per_line = icon_per_line, email_sent = email_sent)

if __name__ == '__main__':
    logging.info("Application starting")
    app.run(debug=True, host="0.0.0.0")