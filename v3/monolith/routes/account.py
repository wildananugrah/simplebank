from controller.account import Account
from flask import request, Blueprint

account = Blueprint("account", __name__)

@account.route("/", methods=["POST"])
def create():
    return Account.create(request.get_json())

@account.route("/", methods=["GET"])
def detail():
    return Account.detail(request.args.get('account_number'))

@account.route("/list/", methods=["GET"])
def list():
    return Account.list(request.args.get('cif_number'))

@account.route("/", methods=["DELETE"])
def delete():
    return Account.delete(request.args.get('account_number'))