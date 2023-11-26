from flask import Flask, request, jsonify
from pymongo.collection import Collection

from db.database import DatabaseConfig
from services.validation import FIELDS_VALIDATION


app = Flask(__name__)
db_config = DatabaseConfig()


@app.route('/get_form', methods=['POST'])
def get_form() -> jsonify:
    try:
        form_data: dict = request.form.to_dict()
        matching_template: str | None = find_matching_template(form_data)
        if matching_template:
            return jsonify({"name": matching_template})
        else:
            typed_fields: dict = type_fields(form_data)
            return jsonify(typed_fields)
    except Exception as e:
        return jsonify({"error": str(e)})


def find_matching_template(data: dict) -> str | None:
    collection: Collection = db_config.get_templates_collection()
    for template in collection.find():
        matching_fields: int = 0
        for field, value in template.items():
            if '_id' == field == 'name':
                continue
            if field in data and data[field] == value:
                matching_fields += 1
        if matching_fields == len(template) - 2:
            return template['name']
    return None


def type_fields(data):
    find_types: dict = {}
    for field_name, value in data.items():
        for type_field, validator in FIELDS_VALIDATION.items():
            if validator(value):
                find_types[field_name] = type_field
                break
            else:
                find_types[field_name] = 'text'
    return find_types


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
