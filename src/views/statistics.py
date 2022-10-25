from flask import Blueprint, redirect, flash
import helper

stats = Blueprint("stats", __name__)


@stats.route("/statistics")
def statistics():
    """Placeholder for route to stats page"""
    if not helper.logged_in():
        flash("Log in to use the application", "error")
        return redirect("/")
    pass
