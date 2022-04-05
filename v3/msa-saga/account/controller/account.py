from dataclasses import dataclass
from model.account import Account as AccountModel
from exception.business_logic_exception import BusinessLogicException
from abc import ABC, abstractmethod
from datetime import datetime
from view.presenter import detail
from flask import jsonify

class Account:

    @staticmethod
    def detail(account_number):
        try:
            print(f"incoming request: {account_number}")
            start = datetime.now()
            account_model = AccountModel()
            account_data = account_model.detail(account_number)
            print(f"outgoing response: {account_data}")
            return detail(account_data, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

    @staticmethod
    def update(json_request):
        try:
            print(f"incoming request: {json_request}")
            start = datetime.now()
            account_model = AccountModel()
            account_data = account_model.update(json_request['account_number'], int(json_request['current_balance']))
            print(f"outgoing response: {account_data}")
            return detail(account_data, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500
    
    @staticmethod
    def update_many(json_request):
        try:
            print(f"incoming request: {json_request}")
            start = datetime.now()
            account_model = AccountModel()
            account_data = account_model.update_many(json_request)
            print(f"outgoing response: {account_data}")
            return detail(account_data, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

    @staticmethod
    def settlement(json_request):
        try:
            print(f"incoming request: {json_request}")
            start = datetime.now()
            account_model = AccountModel()
            account_data = account_model.settlement(json_request['from_account_number'], json_request['to_account_number'], json_request['amount'])
            print(f"outgoing response: {account_data}")
            return detail(account_data, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500
    
    @staticmethod
    def debit(json_request):
        try:
            print(f"incoming request: {json_request}")
            start = datetime.now()
            account_model = AccountModel()
            account_data = account_model.debit(json_request['account_number'], json_request['amount'])
            print(f"outgoing response: {account_data}")
            return detail(account_data, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500
    
    @staticmethod
    def credit(json_request):
        try:
            print(f"incoming request: {json_request}")
            start = datetime.now()
            account_model = AccountModel()
            account_data = account_model.credit(json_request['account_number'], json_request['amount'])
            print(f"outgoing response: {account_data}")
            return detail(account_data, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

    @staticmethod
    def delete(account_number):
        try:
            print(f"incoming request: {account_number}")
            start = datetime.now()
            account_model = AccountModel()
            account_data = account_model.delete(account_number)
            print(f"outgoing response: {account_data}")
            return detail(account_data, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500
    
    @staticmethod
    def list(account_number, skip, limit):
        try:
            print(f"incoming request: {account_number}")
            start = datetime.now()
            account_model = AccountModel()
            account_data = account_model.list(account_number, skip, limit)
            print(f"outgoing response: {account_data}")
            return detail(account_data, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500
    
    @staticmethod
    def create(json_request):
        try:
            print(f"incoming request: {json_request}")
            start = datetime.now()
            account_model = AccountModel()
            account_data = account_model.create(json_request['cif_number'])
            print(f"outgoing response: {account_data}")
            return detail(account_data, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500
