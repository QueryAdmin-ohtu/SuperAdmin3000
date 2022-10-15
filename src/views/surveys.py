import json
from flask import render_template, redirect, request, abort, Blueprint
from flask import current_app as app
import helper
from services.survey_service import survey_service

from logger.logger import Logger

surveys = Blueprint("surveys", __name__)


@surveys.route("/new_survey")
def new():
    """Renders the new survey page
    """
    if not helper.logged_in():
        return redirect("/")

    stored_categories = survey_service.get_all_categories()

    return render_template("surveys/new_survey.html", ENV=app.config["ENV"], categories=stored_categories)


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
    stored_categories = survey_service.get_all_categories()

    return render_template("surveys/view_survey.html", survey=survey,
                           questions=questions, survey_id=survey_id,
                           ENV=app.config["ENV"], categories=stored_categories)


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
        question_id = survey_service.create_question(
            text, survey_id, category_weights)

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
def delete_answer(question_id, answer_id):
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
                           answers=answers)


@surveys.route("/edit_category/<survey_id>/<category_id>", methods=["GET"])
def edit_category_page(survey_id, category_id):
    """  Returns a page for editing or creating a new category.
    """

    # Temporary note for developers:
    # - Currently all categories are available for all surveys.
    # - Target is in the future to make categories survey specific.
    # - However, that cannot be done before Juuso has updated the prod database schema accordingly.
    # - Survey_id is currently passed along, but cannot be used before the prod database update.

    # Returns an empty template for creating a new category
    if category_id == 'new':
        return render_template("surveys/edit_category.html", ENV=app.config["ENV"], survey_id=survey_id)

    # Prefills the template for editing an existing category
    category = survey_service.get_category(category_id)
    name = category[1]
    description = category[2]
    content_links = category[3]
    return render_template("surveys/edit_category.html",
                           ENV=app.config["ENV"], survey_id=survey_id,
                           category_id=category_id, name=name, description=description,
                           content_links=content_links, edit=True)


@surveys.route("/edit_category", methods=["POST"])
def edit_category():
    """ Receives the inputs from the edit_category.html template.
    Stores updated category information to the database.
    """
    if not helper.valid_token(request.form):
        abort(400, 'Invalid CSRF token.')

    survey_id = request.form["survey_id"]
    name = request.form["name"]
    description = request.form["description"]
    stay = request.form["stay"]
    edit = request.form["edit"]
    new_content_links = []

    # Updates existing content links when editing an existing survey
    if edit:
        category_id = request.form["category_id"]
        content_links = survey_service.get_category(category_id)[3]
        for i, item in enumerate(content_links):
            new_content = {
                'url': request.form[f"url_{i}"], 'type': request.form[f"type_{i}"]}
            new_content_links.append(new_content)

    # Adds a new content link, if there is one, to the end
    new_url = request.form["new_url"]
    new_type = request.form["new_type"]
    if new_url and new_type:
        new_content = {'url': new_url, 'type': new_type}
        new_content_links.append(new_content)

    new_content_links_json = json.dumps(new_content_links)

    if edit:
        survey_service.update_category(
            category_id, name, description, new_content_links_json)
    else:
        category_id = survey_service.create_category(
            name, description, new_content_links_json)

    if stay:
        return redirect(f"/edit_category/{survey_id}/{category_id}")
    return redirect(f"/surveys/{survey_id}")


@surveys.route("/delete_category", methods=["POST"])
def delete_category():
    """ Deletes a category from the database.
    Redirects back to survey page if succesfull.
    Shows error message to user if not succesfull.
    """

    if not helper.valid_token(request.form):
        abort(403)

    category_id = request.form["category_id"]
    survey_id = request.form["survey_id"]
    return_value = survey_service.delete_category(category_id)
    if return_value is True:
        return redirect(f"/surveys/{survey_id}")
    return str(return_value)


# Save requestes to the log
@surveys.before_request
def before_request():

    user = helper.current_user()
    Logger(user).log_post_request(request)
