from controller.transaction import *
from flask import request, Blueprint
from pymongo import MongoClient

transaction = Blueprint("transaction", __name__)

@transaction.route("/deposit/", methods=["POST"])
def deposit():
    return Transaction.deposit(request.get_json())

@transaction.route("/reversal/", methods=["POST"])
def reversal():
    return Transaction.reversal(request.get_json())

@transaction.route("/", methods=["GET"])
def detail():
    return Transaction.detail(request.args.get('transaction_type'),request.args.get('account_number'), request.args.get('journal_number'))

@transaction.route("/list/", methods=["GET"])
def list():
    return Transaction.list(request.args.get('cif_number'))

@transaction.route("/transfer/intrabank/", methods=["POST"])
def transfer_intrabank():
    return TransferIntrabank.transfer(request.get_json())

@transaction.route("/debit/", methods=["POST"])
def debit():
    return DebitTransaction.debit(request.get_json())