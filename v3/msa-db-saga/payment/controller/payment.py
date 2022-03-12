from dataclasses import dataclass
from model.payment import Payment as PaymentModel
from model.payment import EletricalBillPayment as EletricalBillPaymentModel
from exception.business_logic_exception import BusinessLogicException
from exception.service_exception import ServiceException
from abc import ABC, abstractmethod
from datetime import datetime
from view.presenter import detail
from flask import jsonify

class Payment:

    @staticmethod
    def list(cif_number):
        try:
            start = datetime.now()
            
            model = PaymentModel()
            payment = model.list(cif_number)

            return detail(payment, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

    @staticmethod
    def detail(transaction_id):
        try:
            start = datetime.now()
            
            model = PaymentModel()
            payment = model.detail(transaction_id)

            return detail(payment, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

class EletricalBillPayment:
    
    @staticmethod
    def inquiry(bill_id):
        try:
            start = datetime.now()
            
            model = EletricalBillPaymentModel()
            payment = model.inquiry(bill_id)

            return detail(payment, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

    @staticmethod
    def pay(json_request):
        try:
            start = datetime.now()
            
            model = EletricalBillPaymentModel()
            model.bill_id = json_request['bill_id']
            model.amount = json_request['amount']
            model.description = json_request['description']
            model.from_account_number = json_request['from_account_number']
            model.cif_number = json_request['cif_number']

            transaction_id = model.pay()
            return detail({ 'transaction_id' : transaction_id }, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500
    
    @staticmethod
    def update(json_request):
        try:
            start = datetime.now()
            model = EletricalBillPaymentModel()            
            
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
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500