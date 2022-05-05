from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from routes.transaction import transaction

app = Flask(__name__)
app.register_blueprint(transaction, url_prefix="/transaction")

if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")