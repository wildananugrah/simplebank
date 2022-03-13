from dataclasses import dataclass
from model.interbank_transfer import InterbankTransfer as InterbankTransferModel
from exception.business_logic_exception import BusinessLogicException
from exception.service_exception import ServiceException
from abc import ABC, abstractmethod
from datetime import datetime
from view.presenter import detail
from flask import jsonify

class InterbankTransfer:

    @staticmethod
    def inquiry(to_account_number, to_bank_code):
        try:
            start = datetime.now()
            
            model = InterbankTransferModel()
            transaction = model.inquiry(to_account_number, to_bank_code)
            
            return detail(transaction, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

    @staticmethod
    def detail(transaction_id):
        try:
            start = datetime.now()
            
            model = InterbankTransferModel()
            transaction = model.detail(transaction_id)
            
            return detail(transaction, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500
    
    @staticmethod
    def list(cif_number):
        try:
            start = datetime.now()
            
            model = InterbankTransferModel()
            print(f"cif_number: {cif_number}")
            transaction = model.list(cif_number)
            
            return detail(transaction, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

    @staticmethod
    def transfer(json_request):
        try:
            start = datetime.now()
            
            model = InterbankTransferModel()
            model.from_account_number = json_request['from_account_number']
            model.to_account_number = json_request['to_account_number']
            model.to_bank_code = json_request['to_bank_code']
            model.cif_number = json_request['cif_number']
            model.amount = int(json_request['amount'])
            model.description = json_request['description']
            transaction_id = model.transfer()
            
            return detail({ 'transaction_id' : transaction_id }, start, 200)

        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except ServiceException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            print(error)
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500
    
    @staticmethod
    def update(json_request):
        try:
            start = datetime.now()
            
            model = InterbankTransferModel()     
            function_list = {
                "DONE" : model.notify,
                "FAILED" : model.update
            }

            function_list[json_request['status']](json_request['transaction_id'], {
                "journal_number" : json_request['journal_number'],
                "status" : json_request['status'],
                "message" : json_request['message']
            }) 
            
            return detail({ 'journal_number' : json_request['journal_number'] }, start, 200)

        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except ServiceException as error:
            return detail({ 'error' : str(error) }, start, 404)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500