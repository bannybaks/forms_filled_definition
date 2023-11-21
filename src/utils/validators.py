import re


FIELD_TYPES = {
    'email': 'email',
    'phone': 'phone',
    'date': 'date',
}


class FieldValidation:
    PATTERN_VALIDATIONS = {
        'email': re.compile(
            r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        ),
        'phone': re.compile(r'^\+7\s\d{3}\s\d{3}\s\d{2}\s\d{2}$'),
        'date': re.compile(r'^(\d{2}\.\d{2}.\d{4}|\d{4}-\d{2}-\d{2})$'),
    }

    def validate_field(self, value, field_type):
        pattern = self.PATTERN_VALIDATIONS.get(field_type)
        return bool(pattern.match(value))


def determine_field_type(field_name):
    return FIELD_TYPES.get(field_name, 'text')
