from flask import render_template, redirect, request, abort, Blueprint
from flask import current_app as app

import helper
from services.survey_service import survey_service

surveys = Blueprint("surveys", __name__)


@surveys.route("/new")
def new():
    """Renders the new survey page
    """
    if not helper.logged_in():
        return redirect("/")

    return render_template("surveys/new.html", ENV=app.config["ENV"])


@surveys.route("/surveys/edit/<survey_id>")
def surveys_edit(survey_id):
    """Renders the edit survey page
    """
    if not helper.logged_in():
        return redirect("/")

    survey = survey_service.get_survey(survey_id)

    return render_template("surveys/edit.html", survey=survey, survey_id=survey_id)


@surveys.route("/surveys/update", methods=["POST"])
def surveys_update():
    """ Form handler for updating an existing survey info
    """

    if not helper.valid_token(request.form):
        abort(403)

    survey_id = request.form["survey_id"]
    name = request.form["name"]
    title = request.form["title"]
    survey = request.form["text"]

    # TODO: Implement the SQL query for updating a survey
    #  result = survey_service.update_survey(survey_id, name, title, text)

    route = f"/surveys/{survey_id}"

    return redirect(route)


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
    survey_id = survey_service.create_survey(name, title, survey)
    route = f"/surveys/{survey_id}"

    return redirect(route)


@surveys.route("/surveys/<survey_id>")
def view_survey(survey_id):
    """ Looks up survey information based
    on the id with a db function and renders
    a page with the info from the survey """

    if not helper.logged_in():
        return redirect("/")

    survey = survey_service.get_survey(survey_id)
    questions = survey_service.get_questions_of_survey(survey_id)

    return render_template("surveys/view_survey.html", survey=survey, questions=questions, survey_id=survey_id)


@surveys.route("/surveys/statistics/<survey_id>")
def surveys_statistics(survey_id):
    """ Open up statistics for the given survey
    """

    if not helper.logged_in():
        return redirect("/")

    survey = survey_service.get_survey(survey_id)

    #  TODO: get statistics
    statistics = "JUGE STATS HERE!"

    return render_template("surveys/statistics.html", survey=survey, statistics=statistics, survey_id=survey_id)

@surveys.route("/surveys/delete/<survey_id>/<question_id>")
def delete_question(question_id, survey_id):
    """Call database query for removal of a single question
    """
    if not helper.logged_in():
        return redirect("/")
    
    survey_service.delete_question_from_survey(question_id)
    return redirect("/surveys/" + survey_id)
