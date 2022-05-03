from controller.account import account_detail, account_create, account_delete, account_list
from flask import request, Blueprint
account = Blueprint("account", __name__)

@account.route("/", methods=["GET"])
def detail():
    return account_detail(request.args.get("account_number"))

@account.route("/", methods=["POST"])
def create():
    return account_create(request.get_json())

@account.route("/", methods=["DELETE"])
def delete():
    return account_delete(request.args.get("account_number"))

@account.route("/list/", methods=["GET"])
def list():
    return account_list(request.args.get("cif_number"), request.args.get("skip"), request.args.get("limit"))