from flask import Flask

from routes.account import account

from mongodb import MongoDB
from db import dbinstance
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.register_blueprint(account, url_prefix="/account")

dbinstance.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, port=3010, host="0.0.0.0", threaded=False)