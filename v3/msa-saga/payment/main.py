from flask import Flask
from routes.payment import payment
from mongodb import MongoDB
from db import dbinstance
from dotenv import load_dotenv
from thread.consumer import channel
from threading import Thread

load_dotenv()

app = Flask(__name__)
app.register_blueprint(payment, url_prefix="/transaction")

dbinstance.init_app(app)

if __name__ == "__main__":
    thread = Thread(target=channel.start_consuming)
    thread.start()
    app.run(debug=True, port=3050, host="0.0.0.0", threaded=False)