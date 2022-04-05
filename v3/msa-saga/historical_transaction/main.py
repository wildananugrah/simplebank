from flask import Flask
from routes.historical_transaction import historical_transaction
from mongodb import MongoDB
from db import dbinstance
from dotenv import load_dotenv
from thread.consumer import channel
from threading import Thread

load_dotenv()

app = Flask(__name__)
app.register_blueprint(historical_transaction, url_prefix="/historical_transaction")

dbinstance.init_app(app)

if __name__ == "__main__":
    thread = Thread(target=channel.start_consuming)
    thread.start()
    app.run(debug=True, port=3030, host="0.0.0.0", threaded=False)
    