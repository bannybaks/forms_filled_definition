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
    def do_GET(self):    #! Удалить после тестирования запуска сервера
        self.send_response(200)
        self.end_headers()
        self.wfile.write(RESPONSE_MESSAGE)

    def do_POST(self):
       pass

def find_matching_template(data):
    pass

def determine_field_type(value):    #! Описать валидацию полей
    pass


if __name__ == '__main__':
    server_destination = (URL_SERVER, PORT_SERVER)
    httpd = HTTPServer(server_destination, RequestHandler)
    print(f'Server is starting in port {PORT_SERVER}')
    httpd.serve_forever()