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

if ENV == 'local':
    print("ENV: local")
    GOOGLE_URI = "http://localhost:5000/google_login"
elif ENV == 'test':
    print("ENV: test")
    GOOGLE_URI = "TO BE DEFINED"
elif ENV == 'prod':
    print("ENV: prod")
    GOOGLE_URI = "https://superadmin3000.herokuapp.com/google_login"
else:
    print("ENV:", ENV)  # Should this throw an error?

# TODO: Create a proper storage for the authorized users
# pylint: disable-next=line-too-long
authorized_google_accounts = ["antti.vainikka36@gmail.com", "jatufin@gmail.com", "me@juan.fi",
# pylint: disable-next=line-too-long
                              "niemi.leo@gmail.com", "oskar.sjolund93@gmail.com", "rami.piik@gmail.com", "siljaorvokki@gmail.com"]

from routes import *

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=PORT)
