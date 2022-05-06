from dataclasses import dataclass
from model.payment import EletricalBillPayment as EletricalBillPaymentModel
from exception.business_logic_exception import BusinessLogicException
from exception.service_exception import ServiceException
from abc import ABC, abstractmethod
from datetime import datetime
from view.presenter import detail
from flask import jsonify

def electrical_billpayment_inquiry(bill_id):
    try:
        start = datetime.now()
        
        model = EletricalBillPaymentModel()
        payment = model.inquiry(bill_id)

        return detail(payment, start, 200)
    except BusinessLogicException as error:
        return detail({ 'error' : str(error) }, start, 400)
    except Exception as error:
        return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

def electrical_billpayment_pay(json_request):
    try:
        start = datetime.now()
        
        model = EletricalBillPaymentModel()
        model.bill_id = json_request['bill_id']
        model.amount = json_request['amount']
        model.description = json_request['description']
        model.from_account_number = json_request['from_account_number']
        model.cif_number = json_request['cif_number']

        journal_number = model.pay()
        return detail({ 'journal_number' : journal_number }, start, 200)
    except BusinessLogicException as error:
        return detail({ 'error' : str(error) }, start, 400)
    except BusinessLogicException as error:
        return detail({ 'error' : str(error) }, start, 400)
    except Exception as error:
        print(error)
        return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500