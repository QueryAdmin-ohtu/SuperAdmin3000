from flask import render_template, redirect, Blueprint
import helper

from logger.logger import Logger

log = Blueprint("logs", __name__)


@log.route("/logs")
def logs():
    """View logs"""
    if not helper.logged_in():
        return redirect("/")

    event_logs = Logger().read_all_events()

    return render_template("logs/logs.html", logs=event_logs)
