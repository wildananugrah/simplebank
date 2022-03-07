from dataclasses import dataclass
from abc import ABC, abstractmethod
from db import dbinstance
from exception.business_logic_exception import BusinessLogicException
from uuid import uuid4
from datetime import datetime

import json
import base64

@dataclass
class CustomerAbstract(ABC):

    """ represent base customer """

    id_number: str = None
    name: str = None
    cif_number: str = None
    is_loggin: bool = None
    session_id: str = None

    @abstractmethod
    def detail(self, key_type, value):
        raise NotImplementedError("detail is not implemented.")

    @abstractmethod
    def create_session_id(self, cif_number):
        raise NotImplementedError("create_session_id is not implemented.")
    
    @abstractmethod
    def update_session_id(self, cif_number, session_id, is_login):
        raise NotImplementedError("update_session_id is not implemented.")
    
    @abstractmethod
    def logout(self, session_id):
        raise NotImplementedError("logout is not implemented.")
    
    @abstractmethod
    def validate_session(self, session_id):
        raise NotImplementedError("validate_session is not implemented.")

@dataclass
class Customer(CustomerAbstract):

    """ represent customer master entiity """
    
    db = dbinstance.get_db().simplebank_db

    def detail(self, key_type, value):
        if key_type in ['id_number', 'cif_number']:
            customer = self.db.customers.find_one({ key_type : value }, {'_id' : False})
            if customer:
                return customer
            else:
                raise BusinessLogicException(f"Can not find the customer key_type: {key_type} value: {value}")
        else:
            raise BusinessLogicException(f"There is no key_type: {key_type}")
    
    def create_session_id(self, cif_number):
        data = json.dumps({
            "cif_number" : cif_number,
            "datetime": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            "uuid": str(uuid4())
        })
        data_bytes = data.encode('ascii')
        base64_bytes = base64.b64encode(data_bytes)
        base64_string = base64_bytes.decode("ascii")

        return base64_string
    
    def update_session_id(self, cif_number, session_id, is_login):
        customer = self.detail('cif_number', cif_number)
        query = { 'cif_number': cif_number }
        new_value = { 'session_id' : session_id, 'is_login' : is_login }
        self.db.customers.update_one( query , { '$set' : new_value })
        return self.detail('cif_number', cif_number)

    def extract_cif_number(self, session_id):
        decode = base64.b64decode(session_id).decode('ascii')
        return json.loads(decode)['cif_number']

    def logout(self, session_id):
        cif_number = self.extract_cif_number(session_id)
        customer = self.detail('cif_number', cif_number)
        self.validate_session(session_id)
        self.update_session_id(cif_number, '', False)
        return self.detail('cif_number', cif_number)

    def validate_session(self, session_id):
        customer = self.detail('cif_number', self.extract_cif_number(session_id))
        if self.db.customers.find_one({ 'cif_number' : customer['cif_number'], 'session_id' : session_id, 'is_login' : True }) is None:
            raise BusinessLogicException(f"Invalid session_id.")
        return customer['is_login']

@dataclass
class CustomerMobile(Customer):

    """ represent customer mobile, user loggin using username and password """

    username: str = None
    password: str = None

    def login(self):
        
        customer = self.db.customers.find_one({ 'username' : self.username, 'password' : self.password }, { '_id' : False })

        if customer is not None:
            session_id = self.create_session_id(customer['cif_number'])
            customer = self.update_session_id(customer['cif_number'], session_id=session_id, is_login=True)
            return customer
        else:
            raise BusinessLogicException(f"Can not find the customer username: {self.username} ")

@dataclass
class CustomerInternetBanking(Customer):

    """ represent customer mobile, user loggin using email and password """

    email: str  = None
    password: str  = None

    def login(self):
        
        customer = self.db.customers.find_one({ 'email' : self.email, 'password' : self.password }, { '_id' : False })
        
        if customer is not None:
            cif_number = customer['cif_number']
            session_id = self.create_session_id(cif_number)
            customer = self.update_session_id(cif_number, session_id=session_id, is_login=True)
            return customer
        else:
            raise BusinessLogicException(f"Can not find the customer email: {self.email} ")

