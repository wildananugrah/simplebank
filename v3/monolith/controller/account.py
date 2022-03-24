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
            start = datetime.now()
            account_model = AccountModel()
            account_data = account_model.detail(account_number)
            return detail(account_data, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

    @staticmethod
    def delete(account_number):
        try:
            start = datetime.now()
            account_model = AccountModel()
            account_data = account_model.delete(account_number)
            return detail(account_data, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500
    
    @staticmethod
    def list(account_number, skip, limit):
        try:
            start = datetime.now()
            account_model = AccountModel()
            account_data = account_model.list(account_number, skip, limit)
            return detail(account_data, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500
    
    @staticmethod
    def create(json_request):
        try:
            start = datetime.now()
            account_model = AccountModel()
            account_data = account_model.create(json_request['cif_number'])
            return detail(account_data, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500
