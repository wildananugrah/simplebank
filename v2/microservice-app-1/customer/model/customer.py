from db import dbinstance
from uuid import uuid4
from datetime import datetime
import json
import base64

class CustomerModel():

    def __init__(self):
        self.db = dbinstance.get_db().simplebank_db
        self.customers = self.db.customers

    def detail_by_cif(self, cif_number):
        customer = self.customers.find_one({ "cif_number" : cif_number }, {'_id': False})
        return customer

    def detail_by_id_number(self, id_number):
        customer = self.customers.find_one({ "id_number": id_number }, {'_id' : False})
        return customer

    def login(self, username, password):
        customer = self.customers.find_one({"username": username, "password" : password}, {'_id' : False})
        return customer

    def logout(self, session_id):
        decode = base64.b64decode(session_id).decode('ascii')
        cif_number = json.loads(decode)['cif_number']
        self.update_session(cif_number, "", False)
        return { "message" : "logout." }

    def validate_session(self, session_id):
        return self.customers.find_one({"session_id" : session_id})
    
    def update_session(self, cif_number, session_id, is_login):
        query = { 'cif_number' : cif_number }
        new_values = { "$set" : { "is_login" : is_login, "session_id" : session_id } }
        self.customers.update_one(query, new_values)