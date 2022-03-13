from dataclasses import dataclass
from model.historical_transaction import HistoricalTransaction as HistTrxModel
from exception.business_logic_exception import BusinessLogicException
from abc import ABC, abstractmethod
from datetime import datetime
from view.presenter import detail
from flask import jsonify

class HistoricalTransaction:

    @staticmethod
    def list(account_number):
        try:
            start = datetime.now()
            hist_model = HistTrxModel()
            historical_trx = hist_model.list(account_number)
            return detail(historical_trx, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500
    
    @staticmethod
    def save(json_request):
        try:
            start = datetime.now()
            
            hist_model = HistTrxModel()
            hist_model.transaction_type = json_request['transaction_type']
            hist_model.account_number = json_request['account_number']
            hist_model.amount = int(json_request['amount'])
            hist_model.journal_number = json_request['journal_number']
            hist_model.current_balance = int(json_request['current_balance'])
            hist_model.description = json_request['description']

            historical_trx = hist_model.save()
            return detail(historical_trx, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500