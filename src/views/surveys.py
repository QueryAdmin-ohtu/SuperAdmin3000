from flask import render_template, redirect, request, abort, Blueprint
from flask import current_app as app

import helper
import db_queries as queries

surveys = Blueprint("surveys", __name__)

@surveys.route("/new")
def new():
    """Renders the new survey page
    """
    if not helper.logged_in():
        return redirect("/")

    return render_template("surveys/new.html", ENV=app.config["ENV"])


@surveys.route("/surveys/edit/<survey_id>")
def edit(survey_id):
    """Renders the edit survey page
    """
    if not helper.logged_in():
        return redirect("/")

    survey = queries.get_survey(survey_id)
    
    return render_template("surveys/edit.html", survey=survey, survey_id=survey_id)

@surveys.route("/create_survey", methods=["POST"])
def create_survey():
    """ Takes arguments from new.html
    and calls a db function using them
    which creates a survey into Surveys
    """

    if not helper.valid_token(request.form):
        abort(403)

    name = request.form["name"]
    title = request.form["title"]
    survey = request.form["survey"]
    survey_id = queries.create_survey(name, title, survey)
    route = "/surveys/" + str(survey_id)

    return redirect(route)


@surveys.route("/surveys/<survey_id>")
def view_survey(survey_id):
    """ Looks up survey information based
    on the id with a db function and renders
    a page with the info from the survey """

    if not helper.logged_in():
        return redirect("/")

    survey = queries.get_survey(survey_id)

    return render_template("surveys/view_survey.html", survey=survey, survey_id=survey_id)
