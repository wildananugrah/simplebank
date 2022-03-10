from pymongo import MongoClient
from sp_config import *
import os

class MongoDB():
    def __init__(self):
        self.app = None
        self.client = None
    
    def init_app(self, app):
        self.app = app
        self.client = (self.get_connection_read(), self.get_connection_write())

    def get_connection_read(self):
        client = MongoClient(MONGODB_READ_HOST)
        return client
    
    def get_connection_write(self):
        client = MongoClient(MONGODB_WRITE_HOST)
        return client

    def get_db(self):
        if not self.client:
            return self.get_connection_read(), self.get_connection_write()
        return self.client