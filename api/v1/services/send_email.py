import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from decouple import config

# Email helper function
MY_EMAIL = config("MY_EMAIL")
MY_PASSWORD = config("MY_PASSWORD")
MAIL_SERVER = config("MAIL_SERVER")


def send_email(subject, recipient, body, body_type='plain'):
    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = MY_EMAIL
    message["To"] = recipient

    part = MIMEText(body, body_type)
    message.attach(part)

    try:
        with smtplib.SMTP_SSL(MAIL_SERVER, 465) as server:
            server.login(MY_EMAIL, MY_PASSWORD)
            server.sendmail(MY_EMAIL, recipient, message.as_string())
            print("Email sent successfully")
    except smtplib.SMTPException as e:
        print(f"Error sending email: {e}")
