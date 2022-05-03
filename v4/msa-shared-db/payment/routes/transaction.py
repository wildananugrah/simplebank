from controller.transaction import transaction_electrical_billpayment_inquiry, transaction_electrical_billpayment_pay
from flask import request, Blueprint
transaction = Blueprint("transaction", __name__)

@transaction.route("/payment/eletrical/", methods=["GET"])
def electrical_billpayment_inquiry():
    return transaction_electrical_billpayment_inquiry(request.args.get('bill_id'))

@transaction.route("/payment/eletrical/", methods=["POST"])
def electrical_billpayment_pay():
    return transaction_electrical_billpayment_pay(request.get_json())