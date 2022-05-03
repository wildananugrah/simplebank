from controller.customer import customer_detail, customer_mobile_login, customer_internet_banking_login, customer_logout
from flask import request, Blueprint
customer = Blueprint("customer", __name__)

@customer.route("/", methods=["GET"])
def detail():
    id_type = request.args.get('key_type')
    value = request.args.get('value')
    return customer_detail(id_type, value)

@customer.route("/mobile/login/", methods=["POST"])
def mobile_login():
    return customer_mobile_login(request.get_json())

@customer.route("/internet_banking/login/", methods=["POST"])
def internet_banking_login():
    return customer_internet_banking_login(request.get_json())

@customer.route("/mobile/logout/", methods=["POST"])
def mobile_logout():
    return customer_logout(request.get_json())

@customer.route("/internet_banking/logout/", methods=["POST"])
def internet_banking_logout():
    return customer_logout(request.get_json())