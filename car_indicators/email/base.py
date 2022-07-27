import smtplib, ssl
from contextlib import contextmanager
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ..config import Settings

context = ssl.create_default_context()

settings = Settings()


def send_email_service(receiver_email: str , message: str):
    with smtplib.SMTP_SSL(
                settings.smtp_address, 
                settings.smtp_port, 
                context=context
            ) as server:
        server.login(settings.smtp_email, settings.smtp_password)

        server.sendmail(settings.smtp_email, receiver_email, message)

def create_message(
        subject: str,
        sender_email: str,
        receiver_email: str,
        text: str,
        html: str = None
    ) -> MIMEMultipart:

    message = MIMEMultipart()
    message["Subject"] = subject
    message["From"] = sender_email
    message["To"] = receiver_email

    message.attach(MIMEText(text, "plain"))
    if html is not None:
        message.attach(MIMEText(html, "html"))

    return message