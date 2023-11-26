from datetime import datetime
from typing import Any, Dict, List

from database import DatabaseConfig


db = DatabaseConfig()
templates_collection: Any = db.get_templates_collection()
templates_collection.delete_many({})
example_templates: List[Dict[str, str | datetime]] = [
    {
        "name": "PersonalInformation",
        "first_name": "Will",
        "last_name": "Bim",
        "email_address": "will.bim@example.com",
        "phone_number": " 7 123 456 78 90"
    },
    {
        "name": "ProductOrder",
        "product_name": "Laptop",
        "quantity": "2",
        "order_date": datetime.now().strftime("%Y-%m-%d")
    },
    {
        "name": "Survey",
        "question_1": "What is your favorite color?",
        "question_2": "How often do you exercise?",
        "question_3": "What is your favorite book?"
    },
    {
        "name": "EventRegistration",
        "event_name": "Tech Conference",
        "participant_name": "Bob Smith",
        "registration_date": datetime.now().strftime("%Y-%m-%d")
    },
    {
        "name": "ContactUs",
        "sender_name": "Emily Brown",
        "sender_email": "emily.brown@example.com",
        "message": "Hello, I have a question about your services."
    }
]
for template in example_templates:
    templates_collection.insert_one(template)
print("The database is filled with sample templates!")
