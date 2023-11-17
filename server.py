from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, Optional
from urllib.parse import parse_qs
import json

from pymongo import MongoClient

from database import db_config
import logging
from logging_conf import configure_logger
from validators import FieldValidation


URL_SERVER = '127.0.0.1'
PORT_SERVER = 8000
PORT_DB = 27017
DB_NAME = 'template_form'
DB_CONNECT = 'mongodb://mongodb:27017/'
LOG_ERROR_VALIDATION = 'Data not valid! {error}'
LOG_ERROR_SERVER = 'Oops... Server error: {error}'
LOG_SEND_REQUESTS_AND_HEADERS = (
    'Sending response with status code {status_code}'
)
LOG_ERROR_REQUEST = 'Error POST request {error}'
ERROR_SERVER_500 = 'Internal server error: {error}'
ERROR_SERVER_400 = 'Data not valid: {error}'
RUN_SERVER_MESSAGE = 'Server is starting in port {port_server}'
RESPONSE_MESSAGE = b'The server is running. GET request processed successfully'

configure_logger()
db = db_config.get_db()


class RequestHandler(BaseHTTPRequestHandler):
    """Handles incoming HTTP requests.

    :param BaseHTTPRequestHandler: Base class for HTTP request handlers.
    """
    def do_POST(self) -> None:
        """Handle POST requests.

        :return: None
        """

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
            logging.error(LOG_ERROR_REQUEST.format(error=error))
            self.send_server_error_response(error)

    def send_response_and_headers(self, status_code: int) -> None:
        """Send HTTP response and headers.

        :param status_code: HTTP status code.
        :return: None
        """
        logging.info(
            LOG_SEND_REQUESTS_AND_HEADERS.format(status_code=status_code)
        )
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def send_success_response(self, response_data: Dict[str, Any]) -> None:
        """Send a success response.

        :param response_data: Data to be sent in the response.
        :return: None
        """
        self.send_response_and_headers(HTTPStatus.OK)
        self.wfile.write(json.dumps(response_data).encode('utf-8'))

    def send_validation_error_response(
        self,
        parsed_data: Dict[str, Any]
    ) -> None:
        """Send a validation error response.

        :param parsed_data: Parsed data from the request.
        :return: None
        """
        try:
            typed_fields_check = self.type_fields(parsed_data)
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
            logging.error(LOG_ERROR_VALIDATION.format(error=error))
            self.send_error(HTTPStatus.INTERNAL_SERVER_ERROR, str(error))

    def send_server_error_response(self, error: Exception) -> None:
        """Send a server error response.

        :param error: The exception that caused the server error.
        :return: None
        """
        logging.error(LOG_ERROR_SERVER.format(error=error))
        self.send_error(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            ERROR_SERVER_500.format(error=error)
        )

    @staticmethod
    def type_fields(
        data: Dict[str, Any],
        type_fields: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Validate and type-check fields.

        :param data: The data to be validated and typed.
        :param type_fields: A dictionary to store the types of each field.
        :return: A dictionary containing the types of each field.
        """
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


def find_matching_template(
    data: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """Find a matching template based on the provided data.

    :param data: The data to find a matching template for.
    :return: A matching template or None if no match is found.
    """
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
    print(RUN_SERVER_MESSAGE.format(port_server=PORT_SERVER))
    httpd.serve_forever()
