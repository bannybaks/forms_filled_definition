from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

from pymongo import MongoClient


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
        content_length = int(self.headers['Content-Length'])
        data = self.rfile.read(content_length)
        parsed_data = parse_qs(data.decode('utf-8'))
        form_template = find_matching_template(parsed_data)

        if form_template:
            ...    #* Вернем имя шаблона
        else:
            ...    #* Вернем в виде словаря данные о полях

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
    if type_fields is None:
        type_fields = {}
    for field, value in data.items():
        field_type = ...    #? здесь буду вызывать валидацию
    return type_fields

def determine_field_type(value):    #! Валидация полей во внешнем модуле 
    pass


if __name__ == '__main__':
    server_destination = (URL_SERVER, PORT_SERVER)
    httpd = HTTPServer(server_destination, RequestHandler)
    print(f'Server is starting in port {PORT_SERVER}')
    httpd.serve_forever()