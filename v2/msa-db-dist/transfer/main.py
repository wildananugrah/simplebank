from flask import Flask

from routes.transfer import transfer

from mongodb import MongoDB
from db import dbinstance
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.register_blueprint(transfer, url_prefix="/transfer")
dbinstance.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, port=3102, host="0.0.0.0")