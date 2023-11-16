from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import json

from pymongo import MongoClient

from validators import FieldValidation


ERROR_SERVER = 'Internal Server Error: {error}'
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
                self.send_response(HTTPServer.OK)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(form_template).encode('utf-8'))
            else:
                typed_fields = type_fields(parsed_data)
                response_dict = {
                    field: field_type
                    for field, field_type in typed_fields.items()
                }
                self.send_response(HTTPStatus.OK)
                self.end_headers()
                self.wfile.write(json.dumps(response_dict).encode('utf-8'))
        except Exception as e:
            self.send_error(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                ERROR_SERVER.format(error=int(e))
            )

def find_matching_template(data):
    for template in db.templates.find(
        {'fields': {'$all': list(data.keys())}}
    ):
        if all(
            data.get(field, [''])[0] == '' for field in template['fields']
        ):
            return template
    return None

def type_fields(data, type_fields=None):
    validators = FieldValidation()
    if type_fields is None:
        type_fields = {}
    for field, value in data.items():
        field_type = validators.validate_field(value[0], field)
        type_fields[field] = field_type
    return type_fields


if __name__ == '__main__':
    server_destination = (URL_SERVER, PORT_SERVER)
    httpd = HTTPServer(server_destination, RequestHandler)
    print(f'Server is starting in port {PORT_SERVER}')
    httpd.serve_forever()