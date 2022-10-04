from flask import Blueprint

stats = Blueprint("stats", __name__)

@stats.route("/statistics")
def statistics():
    """Placeholder for route to stats page"""
    pass
