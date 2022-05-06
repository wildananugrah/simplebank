from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from routes.transaction import transaction
from table.payment import TblPayment
from thread.consumer import channel
from threading import Thread
from database import Base, session, engine

Base.metadata.create_all(engine)

app = Flask(__name__)
app.register_blueprint(transaction, url_prefix="/transaction")

if __name__ == "__main__":
    thread = Thread(target=channel.start_consuming)
    thread.start()
    app.run(debug=True, port=3000, host="0.0.0.0")