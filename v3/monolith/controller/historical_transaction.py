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