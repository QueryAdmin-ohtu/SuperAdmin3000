from datetime import datetime
#from matplotlib import category
from flask import render_template, redirect, request, abort, Blueprint
from flask import current_app as app
import helper
from services.survey_service import survey_service


surveys = Blueprint("surveys", __name__)


@surveys.route("/new_survey")
def new():
    """Renders the new survey page
    """
    if not helper.logged_in():
        return redirect("/")

    return render_template("surveys/new_survey.html", ENV=app.config["ENV"])


@surveys.route("/surveys/edit/<survey_id>")
def surveys_edit(survey_id):
    """Renders the edit survey page
    """
    if not helper.logged_in():
        return redirect("/")

    survey = survey_service.get_survey(survey_id)

    return render_template("surveys/edit_survey.html", survey=survey, survey_id=survey_id, ENV=app.config["ENV"])


@surveys.route("/surveys/update", methods=["POST"])
def surveys_update():
    """ Form handler for updating an existing survey info
    """

    if not helper.valid_token(request.form):
        abort(403)

    survey_id = request.form["survey_id"]
    name = request.form["name"]
    title = request.form["title"]
    description = request.form["description"]

    survey_service.edit_survey(survey_id, name, title, description)
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


@surveys.route("/delete_survey", methods=["POST"])
def delete_survey():
    """ Takes survey id from new.html and calls
    a db function to delete the survey using the id
    and redirects to homepage if deletion succeeded,
    otherwise redirects back to the survey """

    if not helper.valid_token(request.form):
        abort(403)

    survey_id = request.form["id"]
    if survey_service.delete_survey(survey_id):
        return redirect("/")
    return redirect(f"/surveys/{survey_id}")


@surveys.route("/surveys/<survey_id>")
def view_survey(survey_id):
    """ Looks up survey information based
    on the id with a db function and renders
    a page with the info from the survey """

    if not helper.logged_in():
        return redirect("/")

    survey = survey_service.get_survey(survey_id)
    questions = survey_service.get_questions_of_survey(survey_id)

    return render_template("surveys/view_survey.html", survey=survey,
    questions=questions, survey_id=survey_id, ENV=app.config["ENV"])


@surveys.route("/surveys/statistics/<survey_id>")
def surveys_statistics(survey_id):
    """ Open up statistics for the given survey
    """

    if not helper.logged_in():
        return redirect("/")

    survey = survey_service.get_survey(survey_id)

    #  TODO: get statistics
    statistics = "JUGE STATS HERE!"

    return render_template("surveys/statistics.html", survey=survey,
    statistics=statistics, survey_id=survey_id, ENV=app.config["ENV"])


@surveys.route("/add_question", methods=["POST"])
def add_question():
    """ Adds a new question to the database
    """

    if not helper.valid_token(request.form):
        abort(400, 'Invalid CSRF token.')

    categories = survey_service.get_all_categories()
    try:
        category_weights = helper.category_weights_as_json(
            categories, request.form)
    except ValueError:
        return "Invalid weights"
    text = request.form["text"]
    survey_id = request.form["survey_id"]
    question_id = request.form["question_id"]

    if request.form["edit"]:
        survey_service.update_question(
            question_id, text, category_weights)
    else:
        survey_service.create_question(text, survey_id, category_weights)
    return redirect(f"/surveys/{survey_id}")


@surveys.route("/add_answer", methods=["POST"])
def add_answer():
    """ Adds a new answer to a question to the database.
    If the question doesn't exist, it is created first
    """

    if not helper.valid_token(request.form):
        abort(400, 'Invalid CSRF token.')

    question_id = request.form["question_id"]

    if not question_id:
        text = request.form["text"]
        survey_id = request.form["survey_id"]
        categories = survey_service.get_all_categories()
        try:
            category_weights = helper.category_weights_as_json(
                categories, request.form)
        except ValueError:
            return "Invalid weights"
        question_id = survey_service.create_question(text, survey_id, category_weights)

    answer_text = request.form["answer_text"]
    points = request.form["points"]
    if not points:
        points = 0
    try:
        points = float(points)
    except ValueError:
        return "Invalid points"
    survey_service.create_answer(answer_text, points, question_id)
    return redirect(f"/questions/{question_id}")


@surveys.route("/question/delete/<question_id>/<answer_id>", methods=["POST"])
def delete_answer(question_id,answer_id):
    """ Call database query for removal of a single answer
    """
    if not helper.logged_in():
        return redirect("/")

    survey_service.delete_answer_from_question(answer_id)
    return redirect("/questions/" + question_id)


@surveys.route("/<survey_id>/new_question", methods=["GET"])
def new_question(survey_id):
    """  Returns the page for creating a new question.
    """
    stored_categories = survey_service.get_all_categories()
    weights = {}
    return render_template("questions/new_question.html",
                           ENV=app.config["ENV"], categories=stored_categories,
                           survey_id=survey_id, weights=weights)


@surveys.route("/surveys/delete/<survey_id>/<question_id>")
def delete_question(question_id, survey_id):
    """ Call database query for removal of a single question
    """
    if not helper.logged_in():
        return redirect("/")

    survey_service.delete_question_from_survey(question_id)
    return redirect("/surveys/" + survey_id)


@surveys.route("/questions/<question_id>")
def edit_question(question_id):
    """ Returns the page for creating a new question
    where the inputs are filled with the information
    from the question to be edited """
    question = survey_service.get_question(question_id)
    if len(question) < 4:
        return redirect("/")
    text = question[0]
    survey_id = question[1]
    created = question[2]
    weights = question[3]
    answers = survey_service.get_question_answers(question_id)
    if weights:
        weights = helper.json_into_dictionary(question[3])
    stored_categories = survey_service.get_all_categories()
    return render_template("questions/new_question.html",
                           ENV=app.config["ENV"], text=text, survey_id=survey_id,
                           weights=weights, categories=stored_categories,
                           created=created, edit=True, question_id=question_id,
                           answers = answers)
