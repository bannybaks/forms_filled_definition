import logging
from logging.handlers import RotatingFileHandler

LOG_FORMAT = '%(asctime)s [%(levelname)s] - %(message)s'
LOG_FILE = 'server.log'

def configure_file_handler():
    file_handler = RotatingFileHandler(LOG_FILE, backupCount=4)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    return file_handler

def configure_console_handler():
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    return console_handler

def configure_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(configure_file_handler())
    logger.addHandler(configure_console_handler())

if __name__ == '__main__':
    configure_logger()