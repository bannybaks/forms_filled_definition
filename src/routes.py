from flask import request, jsonify

from src import app, mongo
from src.utils.validators import FieldValidation, determine_field_type


@app.route('/get_form', methods=['POST'])
def get_form():
    field_validator = FieldValidation()
    form_data = request.form
    templates = mongo.db.form_template_find()

    for template in templates:
        if all(
            key in form_data and form_data[key] == template[key]
            for key in template.keys()
        ):
            return jsonify({'template_name': template['name']})
    typed_fields = {}
    for key, value in form_data.items():
        field_type = determine_field_type(key)
        is_valid = field_validator.validate_field(value, field_type)

        if not is_valid:
            return jsonify({'error': f'Field {key} is not valid'})

        typed_fields[key] = field_type
    return jsonify(typed_fields)