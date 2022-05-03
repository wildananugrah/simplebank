from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from table.historical_transaction import TblHistoricalTransaction
from routes.transaction import transaction
from database import engine, Base, session

Base.metadata.create_all(engine)

app = Flask(__name__)
app.register_blueprint(transaction, url_prefix="/transaction")

if __name__ == "__main__":
    app.run(debug=True, port=3000, host="0.0.0.0")