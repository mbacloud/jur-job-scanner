import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


LOGOS = {

"poulschmith":"https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Poul_Schmith_logo.png/320px-Poul_Schmith_logo.png",

"kromann":"https://upload.wikimedia.org/wikipedia/commons/thumb/e/e6/Kromann_Reumert_logo.png/320px-Kromann_Reumert_logo.png",

"bech":"https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/Bech-Bruun_logo.png/320px-Bech-Bruun_logo.png"

}


def detect_logo(title):

    t = title.lower()

    if "kromann" in t:
        return LOGOS["kromann"]

    if "bech" in t:
        return LOGOS["bech"]

    if "poul" in t:
        return LOGOS["poulschmith"]

    return ""


def send_email(jobs):

    sender = os.getenv("EMAIL_FROM")
    receiver = os.getenv("EMAIL_TO")
    password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEMultipart("alternative")

    msg["Subject"] = "⚖️ Nye stud.jur jobopslag"
    msg["From"] = sender
    msg["To"] = receiver

    cards = ""

    for title, link in jobs:

        logo = detect_logo(title)

        cards += f"""

        <tr>
        <td style="padding:20px;border:1px solid #eee;border-radius:8px;margin-bottom:20px">

        <img src="{logo}" style="height:40px;margin-bottom:10px"><br>

        <strong style="font-size:16px">{title}</strong><br><br>

        <a href="{link}" 
        style="background:#1a73e8;color:white;padding:10px 18px;
        text-decoration:none;border-radius:6px;font-weight:bold">

        Se stilling

        </a>

        </td>
        </tr>

        """

    html = f"""

    <html>

    <body style="font-family:Arial;background:#f4f6f9;padding:30px">

    <table width="600" align="center" 
    style="background:white;padding:30px;border-radius:10px">

    <tr>
    <td>

    <h2>⚖️ Juridiske studenterjobs fundet</h2>

    <p style="color:#555">
    Nye relevante studenterstillinger inden for jura.
    </p>

    <table width="100%" style="border-collapse:separate;border-spacing:0 15px">

    {cards}

    </table>

    <p style="font-size:12px;color:#999;margin-top:30px">

    Automatisk jobscan<br>
    {datetime.now().strftime("%d %B %Y")}

    </p>

    </td>
    </tr>

    </table>

    </body>

    </html>

    """

    part = MIMEText(html,"html")

    msg.attach(part)

    with smtplib.SMTP_SSL("smtp.gmail.com",465) as server:

        server.login(sender,password)

        server.sendmail(sender,receiver,msg.as_string())import smtplib
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
