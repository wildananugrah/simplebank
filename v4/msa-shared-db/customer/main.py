from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from table.customer import TblCustomer
from table.account import TblAccount

from routes.customer import customer
from database import engine, Base, session

Base.metadata.create_all(engine)

app = Flask(__name__)
app.register_blueprint(customer, url_prefix="/customer")

if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")