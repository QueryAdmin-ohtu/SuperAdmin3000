import json
from flask import render_template, redirect, request, abort, Blueprint, flash
from flask import current_app as app
import helper
from services.survey_service import UserInputError, survey_service
from logger.logger import Logger


surveys = Blueprint("surveys", __name__)


@surveys.route("/surveys/new-survey", methods=["GET"])
def new_survey_view():
    """Renders the new survey page
    """

    stored_categories = survey_service.get_all_categories()

    return render_template("surveys/new_survey.html", ENV=app.config["ENV"], categories=stored_categories)

@surveys.route("/surveys/new-survey", methods=["POST"])
def new_survey_post():
    """Handles creation of new surveys
    """

    name = request.form["name"]
    title = request.form["title"]
    survey = request.form["survey"]
    try:
        survey_id = survey_service.create_survey(name, title, survey)
        route = f"/surveys/{survey_id}"

        flash(f"{name.capitalize()} survey was created", "confirmation")
        return redirect(route)

    except UserInputError as error:
        flash(str(error), "error")
        return redirect(request.base_url)

@surveys.route("/surveys/<survey_id>/edit", methods=["GET"])
def edit_survey_view(survey_id):
    """Renders edit survey page"""

    if not helper.logged_in():
        return redirect("/")

    survey = survey_service.get_survey(survey_id)

    return render_template("surveys/edit_survey.html", survey=survey, ENV=app.config["ENV"])

@surveys.route("/surveys/<survey_id>/edit", methods=["POST"])
def edit_survey_post(survey_id):
    """Handles edit survey request"""

    if not helper.valid_token(request.form):
        abort(403)

    survey_id = request.form["survey_id"]
    name = request.form["name"]
    title = request.form["title"]
    description = request.form["description"]

    survey_service.edit_survey(survey_id, name, title, description)
    route = f"/surveys/{survey_id}"
    return redirect(route)

@surveys.route("/surveys/<survey_id>/delete-survey", methods=["POST"])
def delete_survey(survey_id):
    """ Takes the survey id from a hidden input
    in the form and retrives the survey object
    from the DB. Then comparess that the name of
    the survey and the confirmation the user
    wrote match.

    If names match a db function is called to delete 
    the survey using the id.

    Succeeds: Redirect to home page
    Fails: Redirect back to survey pages"""

    survey_id = request.form["id"]
    confirmation_text = request.form["confirmation-text"]
    survey_to_delete = survey_service.get_survey(survey_id)
    
    if survey_to_delete.name != confirmation_text:
        flash("Confirmation did not match name of survey", "error")
        return redirect(f"/surveys/{survey_id}")

    if survey_service.delete_survey(survey_id):
        flash(f"{survey_to_delete.name.capitalize()} survey was deleted", "confirmation")
        return redirect("/")

    flash("Survey could not be deleted", "error")
    return redirect(f"/surveys/{survey_id}")


@surveys.route("/surveys/<survey_id>")
def view_survey(survey_id):
    """ Looks up survey information based
    on the id with a db function and renders
    a page with the info from the survey """

    survey = survey_service.get_survey(survey_id)
    questions = survey_service.get_questions_of_survey(survey_id)
    categories = survey_service.get_categories_of_survey(survey_id)
    print(categories, flush=True)
    return render_template("surveys/view_survey.html", survey=survey,
                           questions=questions, survey_id=survey_id,
                           ENV=app.config["ENV"], categories=categories)


@surveys.route("/surveys/<survey_id>/statistics")
def survey_statistics(survey_id):
    """ Open up statistics for the given survey
    """

    survey = survey_service.get_survey(survey_id)

    #  TODO: get statistics
    statistics = "JUGE STATS HERE!"

    return render_template("surveys/statistics.html", survey=survey,
                           statistics=statistics, survey_id=survey_id, ENV=app.config["ENV"])


@surveys.route("/surveys/<survey_id>/new-question", methods=["GET"])
def new_question_view(survey_id):
    """  Returns the page for creating a new question.
    """
    if not helper.logged_in():
        return redirect("/")

    survey = survey_service.get_survey(survey_id)
    categories = survey_service.get_categories_of_survey(survey_id)
    weights = {}
    return render_template("questions/edit_question.html",
                           ENV=app.config["ENV"], categories=categories,
                           survey=survey, weights=weights)


@surveys.route("/surveys/<survey_id>/new-question", methods=["POST"])
def new_question_post(survey_id):
    """ Adds a new question or edits an existing question
    """

    text = request.form["text"]
    survey_id = request.form["survey_id"]
    question_id = request.form["question_id"]
    categories = survey_service.get_categories_of_survey(survey_id)

    try:
        category_weights = helper.category_weights_as_json(
            categories, request.form)
    except ValueError:
        return "Invalid weights"

    if request.form["edit"]:
        survey_service.update_question(
            question_id, text, category_weights)
    else:
        question_id = survey_service.create_question(text, survey_id, category_weights)
    return redirect(f"/surveys/{survey_id}/questions/{question_id}")


@surveys.route("/surveys/<survey_id>/questions/<question_id>", methods=["GET"])
def edit_question(survey_id, question_id):
    """ Returns the page for editing the question
    where the inputs are pre-filled"""

    if not helper.logged_in():
        return redirect("/")

    question = survey_service.get_question(question_id)
    if len(question) < 4:
        return redirect("/")
    text = question[0]
    created = question[2]
    weights = question[3]
    answers = survey_service.get_question_answers(question_id)
    if weights:
        weights = helper.json_into_dictionary(question[3])

    survey = survey_service.get_survey(survey_id)    
    categories = survey_service.get_categories_of_survey(survey_id)

    return render_template("questions/edit_question.html",
                           ENV=app.config["ENV"], text=text, survey=survey,
                           weights=weights, categories=categories,
                           created=created, edit=True, question_id=question_id,
                           answers=answers)


@surveys.route("/surveys/<survey_id>/questions/<question_id>/new-answer", methods=["POST"])
def add_answer(survey_id, question_id):
    """ Adds a new answer to a question to the database.
    If the question doesn't exist, it is created first
    """

    question_id = request.form["question_id"]
    answer_text = request.form["answer_text"]
    points = request.form["points"]
    if not points:
        points = 0
    try:
        points = float(points)
    except ValueError:
        return "Invalid points"
    survey_service.create_answer(answer_text, points, question_id)
    return redirect(f"/surveys/{survey_id}/questions/{question_id}")


@surveys.route("/surveys/<survey_id>/question/<question_id>/answers/<answer_id>", methods=["POST"])
def delete_answer(survey_id, question_id, answer_id):
    """ Call database query for removal of a single answer
    """

    survey_service.delete_answer_from_question(answer_id)
    return redirect(f"/surveys/{survey_id}/questions/{question_id}")



@surveys.route("/surveys/delete/<survey_id>/<question_id>", methods=["POST"])
def delete_question(question_id, survey_id):
    """ Call database query for removal of a single question
    """

    survey_service.delete_question_from_survey(question_id)
    return redirect("/surveys/" + survey_id)


@surveys.route("/edit_category/<survey_id>/<category_id>", methods=["GET"])
def edit_category_page(survey_id, category_id):
    """  Returns a page for editing or creating a new category.
    """

    if not helper.logged_in():
        return redirect("/")

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

    survey_id = request.form["survey_id"]
    name = request.form["name"]
    description = request.form["description"]
    edit = request.form["edit"]
    new_content_links = []

    # Updates existing content links when editing an existing survey
    if edit:
        category_id = request.form["category_id"]
        content_links = survey_service.get_category(category_id)[3]
        for i, item in enumerate(content_links):
            new_content = {
                'url': request.form[f"url_{i}"], 'type': request.form[f"type_{i}"]}
            if new_content['url'] and new_content['type']:
                new_content_links.append(new_content)
        new_content_links_json = json.dumps(new_content_links)
        survey_service.update_category(
            category_id, new_content_links_json, name, description)
        # Unclear UX question - Where to return the user when saving changes.
        return redirect(f"/surveys/{survey_id}")

    # Creating a new survey
    new_content_links_json = json.dumps(new_content_links)
    category_id = survey_service.create_category(
        survey_id, name, description, new_content_links_json)
    return redirect(f"/edit_category/{survey_id}/{category_id}")


@surveys.route("/add_content_link", methods=["POST"])
def add_content_link():
    """ Receives the inputs from the edit_category.html template.
    Stores updated content link to the database.
    """
    if not helper.valid_token(request.form):
        abort(400, 'Invalid CSRF token.')

    survey_id = request.form["survey_id"]
    new_content_links = []

    # Updates existing content links in case there are unsaved changes
    category_id = request.form["category_id"]
    content_links = survey_service.get_category(category_id)[3]
    for i, item in enumerate(content_links):
        new_content = {
            'url': request.form[f"url_{i}"], 'type': request.form[f"type_{i}"]}
        new_content_links.append(new_content)

    # Adds new content link to the end
    new_url = request.form["new_url"]
    new_type = request.form["new_type"]
    if new_url and new_type:
        new_content = {'url': new_url, 'type': new_type}
        new_content_links.append(new_content)

    new_content_links_json = json.dumps(new_content_links)

    survey_service.update_category(
        category_id, new_content_links_json)
    return redirect(f"/edit_category/{survey_id}/{category_id}")


@surveys.route("/delete_category", methods=["POST"])
def delete_category():
    """ Deletes a category from the database.
    Redirects back to survey page if succesfull.
    Shows error message to user if not succesfull.
    """

    category_id = request.form["category_id"]
    survey_id = request.form["survey_id"]
    return_value = survey_service.delete_category(category_id)
    if return_value is True:
        flash("Succesfully deleted category", "confirmation")
        return redirect(f"/surveys/{survey_id}")
    
    flash("Could not delete category because it has results linked to it", "error")
    return redirect(f"/surveys/{survey_id}")

@surveys.route("/surveys")
def view_surveys():
    """Redirecting method"""
    return redirect("/")


# Save requestes to the log
@surveys.before_request
def before_request():

    if not helper.logged_in():
        flash("Log in to use the application", "error")
        return redirect("/")

    if request.method == "POST" and not helper.valid_token(request.form):
        abort(400, 'Invalid CSRF token')

    user = helper.current_user()
    Logger(user).log_post_request(request)
