import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection


load_dotenv()


class DatabaseConfig:
    def __init__(self) -> None:
        self.client: MongoClient = MongoClient(
            os.getenv('MONGO_CLIENT')
        )
        self.db: Database = self.client[
            os.getenv('DATABASE_NAME')
        ]
        self.templates_collection: Collection = self.db[
            os.getenv('DATABASE_NAME')
        ]

    def get_templates_collection(self) -> Collection:
        return self.templates_collection
