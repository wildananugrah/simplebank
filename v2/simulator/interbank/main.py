from flask import Flask, jsonify, request
from pymongo import MongoClient
from uuid import uuid4
from datetime import datetime

app = Flask(__name__)
client = MongoClient("mongodb://mongoadmin:secret@mongo:27017/")
db = client.interbank_db

@app.route("/", methods=["POST"])
def create():
    db.accounts.insert_one(request.get_json())
    return jsonify({ "message" : "account has been created!" }), 201

@app.route("/", methods=["GET"])
def inquiry():
    account_number = request.args.get('account_number')
    bank_code = request.args.get('bank_code')

    query = { "account_number" : account_number, 'bank_code' : bank_code }
    print(query)
    account_detail = db.accounts.find_one(query, {"_id" : False})

    return jsonify(account_detail), 201

@app.route("/settlement", methods=["POST"])
def settlement():
    json_request = request.get_json()
    account_number = json_request['account_number']
    bank_code = json_request['bank_code']
    amount = json_request['amount']
    source_bank_code = json_request['source_bank_code']
    source_account_number = json_request['source_account_number']
    transaction_datetime = json_request['transaction_datetime']
    description = json_request['description']
    transaction_id = str(uuid4())
    
    db.settlements.insert_one({
        'account_number' : account_number,
        'bank_code' : bank_code,
        'amount' : amount,
        'source_bank_code': source_bank_code,
        'source_account_number' : source_account_number,
        'source_transaction_datetime' : transaction_datetime,
        'description' : description,
        'transaction_id' : transaction_id,
        'transaction_datetime_received' : datetime.today()
    })

    return jsonify({ 'transaction_id' : transaction_id }), 201

    return jsonify({ "message" : "settled!" })

if __name__ == "__main__":
    app.run(debug=True, port=9000, host="0.0.0.0")