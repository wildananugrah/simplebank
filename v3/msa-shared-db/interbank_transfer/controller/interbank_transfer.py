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
            journal_number = model.transfer()
            
            return detail({ 'journal_number' : journal_number }, start, 200)

        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except ServiceException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500