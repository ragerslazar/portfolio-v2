from typing import Optional

from flask import Flask, render_template, request
from flask_mail import Mail
import logging
from config import Config
from services.mailer import Mailer

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@app.route('/', methods=["GET"])
def home():
    user_agent: str = request.headers.get("User-Agent")
    icon_per_line: int = 6 if "Mobile" in user_agent else 9

    return render_template('index.html', icon_per_line = icon_per_line)

@app.route("/", methods=["POST"])
def home_form():
    email_sent: Optional[bool]
    data = request.get_data()

    if data:
        mailer = Mailer(request, mail, app, logger)
        email_sent = mailer.sendMail()
    else:
        email_sent = False
        logging.error("Mail error")

    return render_template("index.html", email_sent=email_sent)

if __name__ == '__main__':
    logging.info("Application starting")
    app.run(debug=True, host="0.0.0.0")