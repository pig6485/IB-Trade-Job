import requests
from . import config

def send_email(subject, text_content, html_content=None):
    MAILGUN_API_KEY = config.MAILGUN_API_KEY
    MAILGUN_DOMAIN = config.MAILGUN_DOMAIN
    MAILGUN_RECIPIENT = config.MAILGUN_RECIPIENT
    
    if not MAILGUN_API_KEY or not MAILGUN_DOMAIN:
        print("❌ Error: MAILGUN_API_KEY and MAILGUN_DOMAIN environment variables must be set to enable email service.")
        return False

    sender = f"Mailgun Sandbox <postmaster@{MAILGUN_DOMAIN}>"
    request_url = f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages"
    recipient = f"{MAILGUN_RECIPIENT}"

    email_data = {
        "from": sender,
        "to": recipient,
        "subject": subject,
        "text": text_content,
    }

    if html_content:
        email_data["html"] = html_content

    try:
        response = requests.post(
            request_url,
            auth=("api", MAILGUN_API_KEY),
            data=email_data
        )

        if response.status_code == 200:
            print(f"📧 Email successfully sent to {recipient}!")
            return True
        else:
            print(f"❌ Failed to send email. Status Code: {response.status_code}")
            print(f"Error Message: {response.text}")
            return False

    except requests.exceptions.RequestException as error:
        print(f"❌ Network error occurred while sending email: {error}")
        return False
    except Exception as error:
        print(f"❌ An unknown error occurred while sending email: {error}")
        return False