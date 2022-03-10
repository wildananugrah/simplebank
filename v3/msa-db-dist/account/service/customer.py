from dataclasses import dataclass
from exception.business_logic_exception import BusinessLogicException
from sp_config import *
from db import dbinstance

@dataclass
class Customer:

    cif_number: str = None

    db_read, db_write = dbinstance.get_db()

    def detail(self, key_type, value):
        
        if key_type in ['id_number', 'cif_number']:
            customer = self.db_read.simplebank_db.customers.find_one({ key_type : value }, {'_id' : False})
            if customer:
                return customer
            else:
                raise BusinessLogicException(f"Can not find the customer key_type: {key_type} value: {value}")
        else:
            raise BusinessLogicException(f"There is no key_type: {key_type}")