from dataclasses import dataclass
from exception.service_exception import ServiceException
from sp_config import *
import requests, os

@dataclass
class Customer:

    host: str = CUSTOMER_HOST
    cif_number: str = None
    
    invalid_status_code = {
        400 : 'Invalid cif number number',
        404 : 'Interbank cif number does not exist'
    }

    valid_status_code = [200, 201]

    def detail(self, key_type, value):
        
        response = requests.get(f"{self.host}/customer/?key_type={key_type}&value={value}")
        if response is not None and response.status_code in self.valid_status_code:
            return response.json()
        elif response.status_code in self.invalid_status_code:
            raise ServiceException(self.invalid_status_code[response.status_code])
        else:
            raise ServiceException(f"Can not invoke interbank service inquiry.")