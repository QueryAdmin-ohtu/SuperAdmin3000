from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import PORT

app = Flask(__name__)

app.secret_key = getenv("SECRET_KEY")
CLIENT_ID = getenv("GOOGLE_CLIENT_ID")
ENV = getenv("ENVIRONMENT")
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

from views import *

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=PORT)
