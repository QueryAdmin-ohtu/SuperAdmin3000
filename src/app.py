from views import *  # pylint: disable=unused-wildcard-import, wrong-import-order, wildcard-import, cyclic-import

from flask import Flask  # pylint: disable=wrong-import-order
from flask_sqlalchemy import SQLAlchemy  # pylint: disable=wrong-import-order
from config import PORT, load_config

# Create Flask app
app = Flask(__name__)
configs = load_config()
app.config.from_object(configs)

db = SQLAlchemy(app)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=PORT)
