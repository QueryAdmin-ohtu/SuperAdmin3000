from flask import render_template, redirect, Blueprint, flash
from flask import current_app as app
import helper

stats = Blueprint("stats", __name__)


@stats.route("/statistics")
def statistics():
    """Placeholder for route to stats page"""
    if not helper.logged_in():
        flash("Log in to use the application", "error")
        return redirect("/")
    return render_template("surveys/statistics.html", ENV=app.config["ENV"])
