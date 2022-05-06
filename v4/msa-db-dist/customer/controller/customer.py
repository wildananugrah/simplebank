from dataclasses import dataclass
from model.customer import CustomerMobile as CMModel
from model.customer import CustomerInternetBanking as CIBModel
from exception.business_logic_exception import BusinessLogicException
from abc import ABC, abstractmethod
from datetime import datetime
from view.presenter import detail
from flask import jsonify

def customer_detail(key_type, value):
    try:
        start = datetime.now()
        cmmodel = CMModel()
        customer_mobile = cmmodel.detail(key_type, value)
        return detail(customer_mobile, start, 200)
    except BusinessLogicException as error:
        return detail({ 'error' : str(error) }, start, 400)
    except Exception as error:
        return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

def customer_mobile_login(json_request):
    try:
        start = datetime.now()
        cmmodel = CMModel()
        cmmodel.username = json_request['username']
        cmmodel.password = json_request['password']
        customer_mobile = cmmodel.login()

        data = {
            "cif_number": customer_mobile['cif_number'],
            "email": customer_mobile['email'],
            "id_number": customer_mobile['id_number'],
            "is_login": customer_mobile['is_login'],
            "name": customer_mobile['name'],
            "session_id": customer_mobile['session_id'],
            "username": customer_mobile['username']
        }

        return detail(data, start, 200)
    except BusinessLogicException as error:
        return detail({ 'error' : str(error) }, start, 400)
    except Exception as error:
        return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

def customer_logout(json_request):
        try:
            start = datetime.now()
            cmmodel = CMModel()
            customer_mobile = cmmodel.logout(json_request['session_id'])
            return detail(customer_mobile, start, 200)
        except BusinessLogicException as error:
            return detail({ 'error' : str(error) }, start, 400)
        except Exception as error:
            return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500

def customer_interbank_banking_login(json_request):
    try:
        start = datetime.now()
        cibmodel = CIBModel()
        cibmodel.email = json_request['email']
        cibmodel.password = json_request['password']
        customer_mobile = cibmodel.login()

        data = {
            "cif_number": customer_mobile['cif_number'],
            "email": customer_mobile['email'],
            "id_number": customer_mobile['id_number'],
            "is_login": customer_mobile['is_login'],
            "name": customer_mobile['name'],
            "session_id": customer_mobile['session_id'],
            "username": customer_mobile['username']
        }

        return detail(data, start, 200)
    except BusinessLogicException as error:
        return detail({ 'error' : str(error) }, start, 400)
    except Exception as error:
        return jsonify({ 'message' : f'SERVER ERROR: {str(error)}' }), 500