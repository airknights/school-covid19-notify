import logging
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pprint import pprint
import os

logger = logging.getLogger(__name__)


def sendmail(email, school):
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = email
    username_smtp = os.getenv("SMTP_USER")
    password = os.getenv('SMTP_PASS')

    message = MIMEMultipart("alternative")
    message["Subject"] = "Qsmnet covid 19 notification"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = """\
    Hi,
    
    This is a notification from yesterday's data of Ontario covid 19 School.  Based on the data there was an infection
    found in school %s.
    """ % school
    html = """\
    <html>
      <body>
        <p>
            Hi,
        </p>
        <p>
           This is a notification from yesterday's data of Ontario covid 19 School.  Based on the data there was 
           an infection found in school %s.
        </p>
        <p>
        Qsmnet notifications team
        </p>
      </body>
    </html>
    """ % school

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)

    # Create secure connection with server and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("email-smtp.us-east-1.amazonaws.com", 465, context=context) as server:
        server.login(username_smtp, password)
        server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
