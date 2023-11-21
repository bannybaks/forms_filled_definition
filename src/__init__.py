import os

from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv

from src import routes    # noqa


load_dotenv()

app = Flask(__name__)
app.config['MONGO_URI'] = os.getenv('MONGO_URI')
mongo = PyMongo(app)
