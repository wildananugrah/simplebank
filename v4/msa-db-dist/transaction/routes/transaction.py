from controller.transaction import transaction_deposit, transaction_reversal, transaction_list, transaction_intrabank_transfer, transaction_debit, transaction_detail
from flask import request, Blueprint
from pymongo import MongoClient

transaction = Blueprint("transaction", __name__)

@transaction.route("/deposit/", methods=["POST"])
def deposit():
    return transaction_deposit(request.get_json())

@transaction.route("/reversal/", methods=["POST"])
def reversal():
    return transaction_reversal(request.get_json())

@transaction.route("/", methods=["GET"])
def detail():
    return transaction_detail(request.args.get('transaction_type'),request.args.get('account_number'), request.args.get('journal_number'))

@transaction.route("/list/", methods=["GET"])
def list():
    return transaction_list(request.args.get('cif_number'), request.args.get('skip'), request.args.get('limit'))

@transaction.route("/transfer/intrabank/", methods=["POST"])
def transfer_intrabank():
    return transaction_intrabank_transfer(request.get_json())

@transaction.route("/debit/", methods=["POST"])
def debit():
    return transaction_debit(request.get_json())