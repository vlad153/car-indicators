from email import message
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ..config import Settings
from .base import send_email_service, create_message

settings = Settings()

def form_verify_text(token: str) -> str:
    text = f'''
    In order to help maintain the security of your "Car Indicators" account, 
    please verify your email address by using this token: 
    {token}  
    '''
    return text

def form_verify_html(token: str) -> str:

    html = f'''
    <html>
    <body>
      <p>
        In order to help maintain the security of your "Car Indicators" account, 
        please verify your email address by using this token:
      </p> 
        <br />
      <h4>
        {token}
       </h4>
      
    </body>
    </html>
    '''
    return html

def send_verification_email(receiver_email: str, string_token: str):

    text = form_verify_text(string_token)
    html = form_verify_html(string_token)

    message = create_message(
      'Account verification', 
      settings.smtp_email, 
      receiver_email, 
      text, 
      html
      )

    send_email_service(receiver_email, message.as_string())

