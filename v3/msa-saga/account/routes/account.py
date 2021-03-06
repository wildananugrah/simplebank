from controller.account import Account
from flask import request, Blueprint

account = Blueprint("account", __name__)

@account.route("/", methods=["POST"])
def create():
    return Account.create(request.get_json())

@account.route("/settlement/", methods=["POST"])
def settlement():
    return Account.settlement(request.get_json())

@account.route("/debit/", methods=["POST"])
def debit():
    return Account.debit(request.get_json())

@account.route("/credit/", methods=["POST"])
def credit():
    return Account.credit(request.get_json())

@account.route("/", methods=["GET"])
def detail():
    return Account.detail(request.args.get('account_number'))

@account.route("/list/", methods=["GET"])
def list():
    return Account.list(request.args.get('cif_number'), request.args.get('skip'), request.args.get('limit'))

@account.route("/", methods=["PUT"])
def update():
    return Account.update(request.get_json())

@account.route("/many/", methods=["PUT"])
def update_many():
    return Account.update_many(request.get_json())

@account.route("/", methods=["DELETE"])
def delete():
    return Account.delete(request.args.get('account_number'))