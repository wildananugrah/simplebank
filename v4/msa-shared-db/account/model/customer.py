from dataclasses import dataclass
from abc import ABC, abstractmethod
from exception.business_logic_exception import BusinessLogicException
from uuid import uuid4
from datetime import datetime
from table.customer import TblCustomer
from database import session
from sqlalchemy import and_

import json
import base64


@dataclass
class Customer:

    """ represent customer master entiity """
    id_number: str = None
    name: str = None
    cif_number: str = None
    is_loggin: bool = None
    session_id: str = None
    session = session

    def detail(self, key_type, value):
        
        if key_type in ['id_number', 'cif_number']:
            
            customer = None
            if key_type == 'id_number':
                customer = self.session.query(TblCustomer).filter(TblCustomer.id_number == value).first()
            else:
                customer = self.session.query(TblCustomer).filter(TblCustomer.cif_number == value).first()
            
            if customer:
                customer = customer.__dict__
                del customer['_sa_instance_state']
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
        print(f"session_id: {session_id}")
        customer = self.session.query(TblCustomer).filter(TblCustomer.cif_number == cif_number).first()
        customer.session_id = session_id
        session.commit()
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
        customer = self.session.query(TblCustomer).filter(and_(TblCustomer.session_id == session_id, TblCustomer.is_login == False)).first()
        if customer is None:
            raise BusinessLogicException(f"Invalid session_id.")
        return customer

@dataclass
class CustomerMobile(Customer):

    """ represent customer mobile master entiity """
    username: str = None
    password: str = None

    def login(self):

        customer = self.session.query(TblCustomer).filter(and_(TblCustomer.username == self.username, TblCustomer.password == self.password)).first()

        if customer is not None:
            session_id = self.create_session_id(customer.cif_number)
            customer = self.update_session_id(cif_number=customer.cif_number, session_id=session_id, is_login=True)
            return customer
        else:
            raise BusinessLogicException(f"Can not find the customer username: {self.username} ")

@dataclass
class CustomerInternetBanking(Customer):

    """ represent customer internet banking master entiity """
    email: str = None
    password: str = None

    def login(self):
        customer = self.session.query(TblCustomer).filter(and_(TblCustomer.email == self.email, TblCustomer.password == self.password)).first()

        if customer is not None:
            session_id = self.create_session_id(customer.cif_number)
            customer = self.update_session_id(cif_number=customer.cif_number, session_id=session_id, is_login=True)
            return customer
        else:
            raise BusinessLogicException(f"Can not find the customer email: {self.email} ")
