from flask import Flask
from routes.transaction import transaction
from mongodb import MongoDB
from db import dbinstance
from dotenv import load_dotenv
from thread.consumer import channel
from threading import Thread

load_dotenv()

app = Flask(__name__)
app.register_blueprint(transaction, url_prefix="/transaction")

dbinstance.init_app(app)

if __name__ == "__main__":
    thread = Thread(target=channel.start_consuming)
    thread.start()
    app.run(debug=True, port=3020, host="0.0.0.0", threaded=False)