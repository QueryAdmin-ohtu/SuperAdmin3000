from flask import Blueprint, redirect
import helper

stats = Blueprint("stats", __name__)


@stats.route("/statistics")
def statistics():
    """Placeholder for route to stats page"""
    if not helper.logged_in():
        return redirect("/")
    pass
