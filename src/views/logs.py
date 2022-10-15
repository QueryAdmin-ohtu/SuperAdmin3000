from flask import render_template, redirect, Blueprint
from flask import current_app as app
import helper

from logger.logger import Logger

log = Blueprint("logs", __name__)


@log.route("/logs")
def logs():
    if not helper.logged_in():
        return redirect("/")

    logs = Logger().read_all_events()

    return render_template("logs/logs.html", logs=logs)
