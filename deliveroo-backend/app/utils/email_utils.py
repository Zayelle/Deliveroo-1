import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from dotenv import load_dotenv

load_dotenv()

def send_email(to_email, subject, content):
    message = Mail(
        from_email=os.getenv('SENDER_EMAIL'),
        to_emails=to_email,
        subject=subject,
        plain_text_content=content,
    )

    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
        return {
            "status": "Email sent",
            "status_code": response.status_code,
            "body": response.body,
            "headers": dict(response.headers)
        }
    except Exception as e:
        return {"error": str(e)}
