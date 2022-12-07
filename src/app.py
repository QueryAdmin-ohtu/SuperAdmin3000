from flask import Flask
from config import PORT, load_config
from views.home import home
from views.surveys import surveys
from views.statistics import stats
from views.logs import log
from db import db


def create_app():
    """Application factory to create Flask app"""
    app = Flask(__name__)  # pylint: disable=redefined-outer-name
    configs = load_config()
    app.config.from_object(configs)

    app.register_blueprint(home)
    app.register_blueprint(stats)
    app.register_blueprint(surveys)
    app.register_blueprint(log)

    db.init_app(app)
    app.db = db
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=PORT)
