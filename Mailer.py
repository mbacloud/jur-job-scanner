import smtplib
import os
from email.mime.text import MIMEText


def send_email(body):

    msg = MIMEText(body)

    msg["Subject"] = "Nye stud.jur jobs fundet"
    msg["From"] = os.getenv("EMAIL_FROM")
    msg["To"] = os.getenv("EMAIL_TO")

    with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:

        server.login(
            os.getenv("EMAIL_FROM"),
            os.getenv("EMAIL_PASSWORD")
        )

        server.send_message(msg)
