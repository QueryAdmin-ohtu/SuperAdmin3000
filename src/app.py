from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import PORT, load_config

"""Create Flask app"""
app = Flask(__name__)
config = load_config()
app.config.from_object(config)

db = SQLAlchemy(app)

from views import *

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=PORT)
