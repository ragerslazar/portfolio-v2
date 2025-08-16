from typing import Optional

from flask import Flask, render_template, request, flash
from flask_mail import Mail
import logging
from config import Config
from forms.ContactForm import ContactForm
from services.mailer import Mailer

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    form = ContactForm()
    email_sent: Optional[bool] = None

    if request.method == "POST":
        if form.validate_on_submit():
            mailer = Mailer(form, mail, app, logger)
            email_sent = mailer.sendMail()
            flash("Votre message à bien été envoyé !", "success")
        else:
            email_sent = False
            logger.error("Mail error")
            flash("Erreur lors de l'envoi du message. Veuillez réessayer !", "error")

    user_agent: str = request.headers.get("User-Agent")
    icon_per_line: int = 6 if "Mobile" in user_agent else 9

    return render_template("index.html", icon_per_line=icon_per_line, form=form, email_sent=email_sent)

if __name__ == '__main__':
    logging.info("Application starting")
    app.run(debug=True, host="0.0.0.0")