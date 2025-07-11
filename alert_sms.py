import os
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

# Load credentials from .env file
load_dotenv()

ACCOUNT_SID = os.getenv("TWILIO_SID")
AUTH_TOKEN = os.getenv("TWILIO_TOKEN")
FROM_PHONE = os.getenv("TWILIO_FROM")
TO_PHONE = os.getenv("TWILIO_TO")

def send_sms_alert(user, ips):
    body = f"🚨 GENDEF Alert:\nTarget: {user}\nIPs: {', '.join(ips)}"

    url = f"https://api.twilio.com/2010-04-01/Accounts/{ACCOUNT_SID}/Messages.json"
    data = {
        "To": TO_PHONE,
        "From": FROM_PHONE,
        "Body": body
    }

    try:
        response = requests.post(
            url,
            data=urlencode(data),
            auth=(ACCOUNT_SID, AUTH_TOKEN),
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        if response.status_code == 201:
            print("[SMS] Sent successfully")
            return True
        else:
            print(f"[SMS Error] {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"[SMS Exception] {e}")
        return False
