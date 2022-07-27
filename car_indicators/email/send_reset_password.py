from ..config import Settings
from .base import create_message, send_email_service 

settings = Settings()

def form_reset_password_text(token: str):
    text = f'''
    Use this token to reset our password: {token}
    '''
    return text
    

def form_reset_password_html(token: str):
    html = f'''
    <p>
      Use this token to reset our password:
    </p>
    <br />
    <h4>
      {token}
    </h4> 
    '''
    return html


def send_reset_password_email(receiver_email: str, token: str):
    text = form_reset_password_text(token)
    html = form_reset_password_html(token)

    message = create_message(
        'Account reset password',
        settings.smtp_email,
        receiver_email,
        text,
        html
        )
    
    send_email_service(receiver_email, token)