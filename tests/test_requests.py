from datetime import datetime
import os
import requests
import sys
from typing import List, Dict

from dotenv import load_dotenv


LOG_ERROR_SERVER: str = 'Oops... Server error: {error}'
LOG_REQUEST_DATA: str = 'Request data: {request_data}'
LOG_RESPONSE_DATA: str = 'Response: {response_data}'

load_dotenv()

REQUESTS_DATA: List[Dict[str, str | datetime]] = [
    {
        "first_name": "Will",
        "last_name": "Bim",
        "email": "will.bim@example.com",
        "phone": " 7 123 456 78 90"
    },
    {
        "product_name": "Laptop",
        "quantity": "2",
        "order_date": datetime.now().strftime("%Y-%m-%d")
    },
    {
        "question_1": "What is your favorite color?",
        "question_2": "How often do you exercise?",
        "question_3": "What is your favorite book?"
    },
    {
        "event_name": "Tech Conference",
        "participant_name": "Bob Smith",
        "registration_date": datetime.now().strftime("%Y-%m-%d")
    },
    {
        "sender_name": "Emily Brown",
        "sender_email": "emily.brown@example.com",
        "message": "Hello, I have a question about your services."
    }
]

try:
    for data in REQUESTS_DATA:
        response = requests.post(os.getenv('URL'), data=data)
        response.raise_for_status()
        print(LOG_REQUEST_DATA.format(request_data=data))
        print(LOG_RESPONSE_DATA.format(response_data=response.json()))
        print("\n" + "*" * 30 + "\n")

except requests.exceptions.RequestException as error:
    print(LOG_ERROR_SERVER.format(error=error))
    sys.exit()
