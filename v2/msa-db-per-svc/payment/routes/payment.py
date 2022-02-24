from controller.payment import *
from flask import request, Blueprint
from pymongo import MongoClient

payment = Blueprint("payment", __name__)

@payment.route("/bill/inquiry/", methods=["GET"])
def inquiry_billpayment():
    return PaymentController().inquiry_billing(request.args.get('bill_id'))

@payment.route("/bill/payment", methods=["POST"])
def payment_billpayment():
    return PaymentController().pay_billing(request.get_json())

@payment.route("/list", methods=["GET"])
def payment_list():
    return PaymentController().list(request.args.get("cif_number"))

@payment.route("/detail", methods=["GET"])
def payment_detail():
    return PaymentController().detail(request.args.get("transaction_id"))

@payment.route("/update", methods=["POST"])
def payment_update():
    return PaymentController().update(request.get_json())

@payment.route("/update/reversal", methods=["POST"])
def payment_update_reversal():
    return PaymentController().update_reversal(request.get_json())