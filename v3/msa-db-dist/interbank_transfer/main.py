from flask import Flask

from routes.interbank_transfer import interbank_transfer

from mongodb import MongoDB
from db import dbinstance
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.register_blueprint(interbank_transfer, url_prefix="/transaction")

dbinstance.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, port=3040, host="0.0.0.0", threaded=False)