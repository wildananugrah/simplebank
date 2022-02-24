# from account.controller.account import *
from flask import request, Blueprint
from controller.account import *

account = Blueprint("account", __name__)

@account.route("/", methods=["POST"])
@account.route("", methods=["POST"])
def create():
    return AccountController().create(request.get_json())

@account.route("/", methods=["DELETE"])
@account.route("", methods=["DELETE"])
def delete():
    return AccountController().delete(request.args.get('account_number'))

@account.route("/", methods=["GET"])
@account.route("", methods=["GET"])
def detail():
    return AccountController().detail(request.args.get('account_number'))

@account.route("/list", methods=["GET"])
@account.route("/list/", methods=["GET"])
def list():
    return AccountController().list(request.args.get('cif_number'))

@account.route("/historical_transaction", methods=['GET'])
@account.route("/historical_transaction/", methods=['GET'])
def historical_transaction():
    return AccountController().historical_transaction(request.args.get('account_number'))

@account.route("/deposit", methods=['POST'])
@account.route("/deposit/", methods=['POST'])
def deposit():
    return AccountController().deposit(request.get_json())

# @account.route("/transfer", methods=['POST'])
# @account.route("/transfer/", methods=['POST'])
# def transfer():
#     return AccountController().transfer(request.get_json())

# @account.route("/debit", methods=['POST'])
# @account.route("/debit/", methods=['POST'])
# def debit():
#     return AccountController().debit(request.get_json())

# @account.route("/transfer/interbank", methods=['POST'])
# @account.route("/transfer/interbank/", methods=['POST'])
# def interbank():
#     return AccountController().debit(request.get_json())

# @account.route("/reversal/", methods=["POST"])
# def reversal():
#     return AccountController().reversal(request.get_json())