from controller.historical_transaction import HistoricalTransaction
from flask import request, Blueprint

historical_transaction = Blueprint("historical_transaction", __name__)

@historical_transaction.route("/", methods=["GET"])
def find():
    return HistoricalTransaction.list(request.args.get('account_number'), request.args.get('skip'), request.args.get('limit'))

@historical_transaction.route("/", methods=["POST"])
def save():
    return HistoricalTransaction.save(request.get_json())