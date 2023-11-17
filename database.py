from pymongo import MongoClient


class DatabaseConfig:
    def __init__(self, db_connect, db_name):
        self.db_connect = db_connect
        self.db_name = db_name

    def get_db(self):
        client = MongoClient(self.db_connect)
        return client[self.db_name]


db_config = DatabaseConfig(
    db_connect="mongodb://mongodb:27017/",
    db_name="template_form"
)
