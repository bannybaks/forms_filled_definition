from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json

from pymongo import MongoClient

from validators import FieldValidation


ERROR_SERVER_500 = 'Internal server error: {error}'
ERROR_SERVER_400 = 'Data not valid: {error}'
RESPONSE_MESSAGE = b'The server is running. GET request processed successfully'
URL_SERVER = '127.0.0.1'
PORT_SERVER = 8000
PORT_DB = 27017
DB_NAME = 'template_form'
DB_CONNECT = 'mongodb://mongodb:27017/'


client = MongoClient(DB_CONNECT)
db = client[DB_NAME]


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            data = self.rfile.read(content_length)
            parsed_data = parse_qs(data.decode('utf-8'))
            form_template = find_matching_template(parsed_data)
            if form_template:
                self.send_success_response(form_template)
            else:
                self.send_validation_error_response(parsed_data)
        except Exception as error:
            self.send_server_error_response(error)

    def send_response_and_headers(self, status_code):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def send_success_response(self, response_data):
        self.send_response_and_headers(HTTPStatus.OK)
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

    def send_validation_error_response(self, parsed_data):
        try:
            typed_fields_check = type_fields(parsed_data)
            if 'error' in typed_fields_check:
                status_code = HTTPStatus.BAD_REQUEST.value
                error_message = typed_fields_check['error']
                self.send_response_and_headers(status_code)
                self.wfile.write(
                    json.dumps({'error': error_message}).encode('utf-8')
                )
            else:
                status_code = HTTPStatus.OK.value
                self.send_success_response(typed_fields_check)
        except (ValueError, TypeError) as error:
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, str(error))

    def send_server_error_response(self, error):
        self.send_error(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            ERROR_SERVER_500.format(error=error)
        )

    @staticmethod
    def type_fields(data, type_fields=None):
        validators = FieldValidation()
        try:
            if type_fields is None:
                type_fields = {}
            for field, value in data.items():
                field_type = validators.validate_field(value[0], field)
                type_fields[field] = field_type
            return type_fields
        except ValueError as error:
            return {'error': ERROR_SERVER_400.format(error=error)}
        except Exception as error:
            return {'error': ERROR_SERVER_500.format(error=error)}


def find_matching_template(data):
    for template in db.templates.find(
        {'fields': {'$all': list(data.keys())}}
    ):
        if all(
            data.get(field, [''])[0] == '' for field in template['fields']
        ):
            return template
    return None


if __name__ == '__main__':
    server_destination = (URL_SERVER, PORT_SERVER)
    httpd = HTTPServer(server_destination, RequestHandler)
    print(f'Server is starting in port {PORT_SERVER}')
    httpd.serve_forever()