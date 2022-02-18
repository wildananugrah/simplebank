from flask import Flask, jsonify, request
from pymongo import MongoClient
from uuid import uuid4
from datetime import datetime
import random, string

app = Flask(__name__)
client = MongoClient("mongodb://mongoadmin:secret@mongo:27017/")
db = client.billpayment_db

def find_bill_id(bill_id):
    return db.billings.find_one({ "bill_id" : bill_id }, {'_id' : False})

def generate_billing(bill_id = "", size=12):
    bill_id = ''.join(random.choice(string.digits) for _ in range(size))
    db_bill_id = find_bill_id(bill_id)
    if db_bill_id:
        generate_bill_id(bill_id)
    return bill_id

@app.route("/create_billing", methods=["POST"])
def create_billing():
    bill_id = generate_billing()

    content = {
        'detail' : request.get_json(),
        'bill_id' : bill_id,
        'status_payment' : 'UNPAID',
        'incoming_request': ''
    }

    db.billings.insert_one(content)
    detail = db.billings.find_one({ 'bill_id' : bill_id }, {'_id' : False})

    return jsonify(detail), 201


@app.route("/", methods=["GET"])
def inquiry():
    bill_id = request.args.get("bill_id")
    return jsonify(db.billings.find_one({ 'bill_id' : bill_id }, {'_id' : False})), 201

@app.route("/", methods=["POST"])
def payment():
    json_request = request.get_json()
    bill_id = json_request['bill_id']

    query = { 'bill_id' : bill_id }
    newvalues = { 'status_payment' : 'PAID', "incoming_request" : json_request}

    db.billings.update_one(query, { '$set' : newvalues })

    return jsonify(db.billings.find_one({ 'bill_id' : bill_id }, {'_id' : False})), 201

if __name__ == "__main__":
    app.run(debug=True, port=9010, host="0.0.0.0")