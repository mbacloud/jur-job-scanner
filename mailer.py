import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


def extract_company(title, link):

    domain = link.split("/")[2]

    company = domain.replace("www.", "").split(".")[0]

    company = company.replace("-", " ").title()

    return company


def clean_title(title):

    # fjern lange beskrivelser
    if "?" in title:
        title = title.split("?")[0]

    if "." in title:
        title = title.split(".")[0]

    if "Read more" in title:
        title = title.split("Read more")[0]

    title = title.strip()

    # forkort typiske formuleringer
    title = title.replace("Juridisk student og erhvervsjuridisk student", "Stud.jur")

    return title


def send_email(jobs):

    sender = os.getenv("EMAIL_FROM")
    receiver = os.getenv("EMAIL_TO")
    password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEMultipart("alternative")

    msg["Subject"] = "⚖️ Nye stud.jur jobopslag"
    msg["From"] = sender
    msg["To"] = receiver

    rows = ""

    for title, link in jobs:

        company = extract_company(title, link)
        title = clean_title(title)

        rows += f"""
        <tr>
        <td style="padding:18px;border:1px solid #e6e6e6;border-radius:8px;background:#fafafa">

        <div style="font-size:13px;color:#666">
        {company}
        </div>

        <div style="font-size:16px;font-weight:bold;margin-top:3px">
        {title}
        </div>

        <div style="margin-top:12px">
        <a href="{link}"
        style="background:#1a73e8;color:white;padding:8px 16px;
        text-decoration:none;border-radius:6px;font-weight:bold;font-size:13px">

        Se stilling

        </a>
        </div>

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

    {rows}

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

    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:

        server.login(sender, password)

        server.sendmail(sender, receiver, msg.as_string())
