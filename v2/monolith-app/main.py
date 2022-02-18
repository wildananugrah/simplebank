from flask import Flask

from routes.customer import customer
from routes.account import account
from routes.transfer import transfer
from routes.payment import payment

from mongodb import MongoDB
from db import dbinstance

app = Flask(__name__)
app.register_blueprint(customer, url_prefix="/customer")
app.register_blueprint(account, url_prefix="/account")
app.register_blueprint(transfer, url_prefix="/transfer")
app.register_blueprint(payment, url_prefix="/payment")
dbinstance.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")