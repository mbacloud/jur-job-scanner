import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
from urllib.parse import urlparse


def extract_company(title, link):

    try:
        domain = urlparse(link).netloc

        company = domain.replace("www.", "").split(".")[0]

        return company.replace("-", " ").title()

    except:
        return "Ukendt virksomhed"


def logo_url(link):

    try:
        domain = urlparse(link).netloc

        return f"https://logo.clearbit.com/{domain}"

    except:
        return ""


def clean_title(title):

    if "?" in title:
        title = title.split("?")[0]

    if "Read more" in title:
        title = title.split("Read more")[0]

    return title.strip()

def clean_title(title):

    title = title.lower()

    # standard jobtitler
    if "stud.jur" in title:
        return "Stud.jur"

    if "studentermedhjælper" in title:
        return "Studentermedhjælper"

    if "juridisk student" in title:
        return "Stud.jur"

    if "legal student" in title:
        return "Stud.jur"

    # fjern marketing-tekst
    remove_words = [
        "are you a student",
        "club",
        "offers students",
        "unique opportunities",
        "read more",
        "click here"
    ]

    for word in remove_words:
        title = title.replace(word, "")

    title = title.strip()

    # hvis titlen stadig er lang → klip den
    if len(title) > 60:
        title = title[:60] + "..."

    return title.title()

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

        company = extract_company(title, link)
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

    <!-- HERO -->

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

    <!-- JOB CARDS -->

    {cards}

    <!-- FOOTER -->

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
