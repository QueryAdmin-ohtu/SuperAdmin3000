from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import PORT, load_config

# Create Flask app
app = Flask(__name__)
configs = load_config()
app.config.from_object(configs)

db = SQLAlchemy(app)

# This is here, because the views.py imports from app
from views import *  # pylint: disable=unused-wildcard-import, wrong-import-order, wrong-import-position, wildcard-import, cyclic-import

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=PORT)
