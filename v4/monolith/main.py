from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from table.customer import TblCustomer
from table.account import TblAccount
from table.historical_transaction import TblHistoricalTransaction
from table.transaction import TblTransaction

from routes.customer import customer
from routes.account import account
from routes.historical_transaction import historical_transaction
from routes.transaction import transaction

from database import engine, Base, session

Base.metadata.create_all(engine)

app = Flask(__name__)
app.register_blueprint(customer, url_prefix="/customer")
app.register_blueprint(account, url_prefix="/account")
app.register_blueprint(historical_transaction, url_prefix="/historical_transaction")
app.register_blueprint(transaction, url_prefix="/transaction")

if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")