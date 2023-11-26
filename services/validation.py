from datetime import datetime
from typing import Dict, Callable
import re


def is_valid_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def is_valid_phone(phone_str: str) -> bool:
    if re.fullmatch(
        r'^7\s\d{3}\s\d{3}\s\d{2}\s\d{2}$', phone_str.lstrip(' ')
    ):
        return True
    return False


def is_valid_email(email_str: str) -> bool:
    if re.match(
        r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
        email_str
    ):
        return True
    return False


FIELDS_VALIDATION: Dict[str, Callable] = {
    'date': is_valid_date,
    'phone': is_valid_phone,
    'email': is_valid_email,
}
