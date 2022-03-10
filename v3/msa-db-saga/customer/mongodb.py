from pymongo import MongoClient
from sp_config import *
import os

class MongoDB():
    def __init__(self):
        self.app = None
        self.client = None
    
    def init_app(self, app):
        self.app = app
        self.client = self.get_connection()

    def get_connection(self):
        client = MongoClient(MONGODB_HOST)
        
        return client

    def get_db(self):
        if not self.client:
            return self.get_connection()
        return self.client