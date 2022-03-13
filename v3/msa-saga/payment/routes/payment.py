from controller.payment import EletricalBillPayment, Payment
from flask import request, Blueprint
from pymongo import MongoClient

payment = Blueprint("payment", __name__)

@payment.route("/payment/eletrical/", methods=["GET"])
def inquiry_eletrical_payment():
    return EletricalBillPayment.inquiry(request.args.get('bill_id'))

@payment.route("/payment/eletrical/", methods=["POST"])
def pay_eletrical_payment():
    return EletricalBillPayment.pay(request.get_json())

@payment.route("/payment/eletrical/update/", methods=["POST"])
def update_eletrical_update():
    return EletricalBillPayment.update(request.get_json())

@payment.route("/payment/detail/", methods=["GET"])
def payment_detail():
    return Payment.detail(request.args.get('transaction_id'))

@payment.route("/payment/list/", methods=["GET"])
def payment_list():
    return Payment.list(request.args.get('cif_number'))