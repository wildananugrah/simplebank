from flask import Flask

from routes.customer import customer

from mongodb import MongoDB
from db import dbinstance
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.register_blueprint(customer, url_prefix="/customer")

dbinstance.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")