from flask import render_template, redirect, Blueprint
from flask import current_app as app
import helper

log = Blueprint("logs", __name__)

@log.route("/logs")
def logs():
    if not helper.logged_in():
        return redirect("/")
    return render_template("logs/logs.html")