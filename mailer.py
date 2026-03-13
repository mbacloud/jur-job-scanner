import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


LOGO_MAP = {
"bruunhjejle": "https://bruunhjejle.dk/media/1496/logo.svg",
"kromannreumert": "https://kromannreumert.com/-/media/images/global/logo.svg",
"bechbruun": "https://www.bechbruun.com/-/media/images/logo.svg",
"poulschmith": "https://jobs.poulschmith.dk/-/media/poul-schmith-logo.svg",
"accura": "https://accura.dk/wp-content/themes/accura/assets/logo.svg",
"njord": "https://www.njordlaw.com/-/media/images/logo.svg",
"schjodt": "https://schjodt.com/-/media/images/logo.svg"
}


def extract_company(link):

    domain = link.split("/")[2].replace("www.","")

    return domain.split(".")[0].replace("-", " ").title()


def logo_url(link):

    domain = link.split("/")[2].replace("www.","")
    key = domain.split(".")[0]

    if key in LOGO_MAP:
        return LOGO_MAP[key]

    return f"https://logo.clearbit.com/{domain}"


def clean_title(title):

    title = title.strip()

    remove = [
        "are you a student",
        "club",
        "read more",
        "click here",
        "offers students",
        "unique opportunities"
    ]

    lower = title.lower()

    for word in remove:
        lower = lower.replace(word,"")

    title = lower.strip().title()

    departments = [
        "M&A",
        "Corporate",
        "Competition",
        "Banking",
        "Dispute",
        "Tax",
        "IP",
        "Employment"
    ]

    for dept in departments:
        if dept.lower() in title.lower():
            return f"Stud.jur – {dept}"

    if "stud" in title.lower():
        return "Stud.jur"

    return title


def send_email(jobs):

    sender = os.getenv("EMAIL_FROM")
    receiver = os.getenv("EMAIL_TO")
    password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEMultipart("alternative")

    msg["Subject"] = "⚖️ Nye Stud.jur jobopslag"
    msg["From"] = sender
    msg["To"] = receiver

    cards = ""

    for title, link in jobs:

        company = extract_company(link)
        title = clean_title(title)
        logo = logo_url(link)

        cards += f"""
        <tr>
        <td style="padding:20px 0">

        <table width="100%" style="
        background:white;
        border-radius:10px;
        border:1px solid #e8e8e8;
        padding:20px">

        <tr>

        <td width="60">

        <img src="{logo}" 
        style="height:40px;width:40px;border-radius:6px">

        </td>

        <td>

        <div style="font-size:13px;color:#666">
        {company}
        </div>

        <div style="font-size:17px;font-weight:bold">
        {title}
        </div>

        <div style="margin-top:12px">

        <a href="{link}" style="
        background:#1a73e8;
        color:white;
        padding:9px 16px;
        text-decoration:none;
        border-radius:6px;
        font-weight:bold;
        font-size:13px">

        Se stilling

        </a>

        </div>

        </td>

        </tr>

        </table>

        </td>
        </tr>
        """

    html = f"""
    <html>
    <body style="
    font-family:Arial,Helvetica,sans-serif;
    background:#f4f6f9;
    padding:40px">

    <table width="600" align="center" style="background:#f4f6f9">

    <tr>
    <td style="
    background:white;
    padding:30px;
    border-radius:10px;
    text-align:center">

    <h1 style="margin:0">
    ⚖️ Stud.jur Job Scanner
    </h1>

    <p style="color:#666;margin-top:10px">
    Nye juridiske studenterjobs er fundet
    </p>

    </td>
    </tr>

    {cards}

    <tr>
    <td style="
    text-align:center;
    font-size:12px;
    color:#999;
    padding-top:20px">

    Automatisk jobscan<br>
    {datetime.now().strftime("%d %B %Y")}

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
