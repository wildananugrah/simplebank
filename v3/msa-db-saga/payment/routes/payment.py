from controller.transaction import *
from flask import request, Blueprint
from pymongo import MongoClient

payment = Blueprint("payment", __name__)

@payment.route("/payment/eletrical/", methods=["GET"])
def inquiry_eletrical_payment():
    return EletricalBillPayment.inquiry(request.args.get('bill_id'))

@payment.route("/payment/eletrical/", methods=["POST"])
def pay_eletrical_payment():
    return EletricalBillPayment.pay(request.get_json())