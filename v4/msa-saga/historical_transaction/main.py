from dotenv import load_dotenv
load_dotenv()

from flask import Flask
from thread.consumer import channel
from threading import Thread
from routes.historical_transaction import historical_transaction
from database import engine, Base, session

Base.metadata.create_all(engine)

app = Flask(__name__)
app.register_blueprint(historical_transaction, url_prefix="/historical_transaction")

if __name__ == "__main__":
    thread = Thread(target=channel.start_consuming)
    thread.start()
    app.run(debug=True, port=3000, host="0.0.0.0")