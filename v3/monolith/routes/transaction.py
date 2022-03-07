from controller.transaction import *
from flask import request, Blueprint
from pymongo import MongoClient

transaction = Blueprint("transaction", __name__)

@transaction.route("/deposit/", methods=["POST"])
def deposit():
    return Transaction.deposit(request.get_json())

@transaction.route("/", methods=["GET"])
def detail():
    return Transaction.detail(request.args.get('transaction_type'),request.args.get('account_number'), request.args.get('journal_number'))

@transaction.route("/list/", methods=["GET"])
def list():
    return Transaction.list(request.args.get('cif_number'))

@transaction.route("/transfer/intrabank/", methods=["POST"])
def transfer_intrabank():
    return TransferIntrabank.transfer(request.get_json())

@transaction.route("/transfer/interbank/", methods=["GET"])
def inquiry_interbank():
    return TransferInterbank.inquiry(request.args.get('to_account_number'), request.args.get('to_bank_code'))

@transaction.route("/transfer/interbank/", methods=["POST"])
def transfer_interbank():
    return TransferInterbank.transfer(request.get_json())

@transaction.route("/payment/eletrical/", methods=["GET"])
def inquiry_eletrical_payment():
    return EletricalBillPayment.inquiry(request.args.get('bill_id'))

@transaction.route("/payment/eletrical/", methods=["POST"])
def pay_eletrical_payment():
    return EletricalBillPayment.pay(request.get_json())