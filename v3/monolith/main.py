from flask import Flask

from routes.customer import customer
from routes.account import account
from routes.transaction import transaction
from routes.historical_transaction import historical_transaction

from mongodb import MongoDB
from db import dbinstance
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.register_blueprint(customer, url_prefix="/customer")
app.register_blueprint(account, url_prefix="/account")
app.register_blueprint(transaction, url_prefix="/transaction")
app.register_blueprint(historical_transaction, url_prefix="/historical_transaction")

dbinstance.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")