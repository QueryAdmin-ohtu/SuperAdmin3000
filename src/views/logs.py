from flask import render_template, redirect, Blueprint, flash
import helper

from logger.logger import Logger

log = Blueprint("logs", __name__)


@log.route("/logs")
def logs():
    """View logs"""
    if not helper.logged_in():
        flash("Log in to use the application", "error")
        return redirect("/")

    event_logs = Logger().read_all_events()
    event_logs.reverse()
    
    return render_template("logs/logs.html", logs=event_logs, reverse=False)

@log.route("/logs/oldestfirst")
def logs_reversed():
    if not helper.logged_in():
        flash("Log in to use the application", "error")
        return redirect("/")

    event_logs = Logger().read_all_events()
    
    return render_template("logs/logs.html", logs=event_logs, reverse=True)
