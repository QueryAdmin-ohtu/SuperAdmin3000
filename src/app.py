from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import PORT

app = Flask(__name__)
app.config.from_pyfile("config.py")

db = SQLAlchemy(app)

from views import *

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=PORT)
