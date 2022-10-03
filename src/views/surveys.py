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

    return render_template("new.html", ENV=app.config["ENV"])


@surveys.route("/edit")
def edit():
    """Renders the edit survey page
    """
    if not helper.logged_in():
        return redirect("/")

    return render_template("edit.html", ENV=app.config["ENV"])

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

    survey = queries.get_survey(survey_id)

    if survey is False:
        report = "There is no survey by that id"

        return render_template("view_survey.html", no_survey=report,
                               ENV=app.config["ENV"])

    survey_questions = queries.get_questions_of_questionnaire(survey_id)

    return render_template("view_survey.html", name=survey[1],
                           created=survey[2], updated=survey[3], title=survey[4],
                           text=survey[5], questions=survey_questions, ENV=app.config["ENV"])
