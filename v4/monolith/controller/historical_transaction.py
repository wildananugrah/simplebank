from dataclasses import dataclass
from model.historical_transaction import HistoricalTransaction
from exception.business_logic_exception import BusinessLogicException
from abc import ABC, abstractmethod
from datetime import datetime
from view.presenter import view_detail
from flask import jsonify

def historical_transaction_save(json_request):
    try:
        start = datetime.now()
        model = HistoricalTransaction()
        model.transaction_type = json_request['transaction_type']
        model.account_number = json_request['account_number']
        model.amount = int(json_request['amount'])
        model.journal_number = json_request['journal_number']
        model.current_balance = int(json_request['current_balance'])
        model.description = json_request['description']
        historical_transaction = model.save()

        return view_detail(historical_transaction, start)
    except BusinessLogicException as error:
        return view_detail({ 'error' : str(error) }, start, 400)
    except Exception as error:
        return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

def historical_transaction_list(account_number, skip, limit):
    try:
        start = datetime.now()
        model = HistoricalTransaction()
        historical_transaction = model.list(account_number, skip, limit)

        return view_detail(historical_transaction, start)
    except BusinessLogicException as error:
        return view_detail({ 'error' : str(error) }, start, 400)
    except Exception as error:
        return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500