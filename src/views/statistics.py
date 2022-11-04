from flask import render_template, redirect, Blueprint, flash
from flask import current_app as app
import helper
from services.survey_service import survey_service

stats = Blueprint("stats", __name__)


@stats.route("/surveys/<survey_id>/statistics", methods=["GET"])
def statistics(survey_id):
    """Shows the statistics for the specific survey"""
    # TODO: This should be removed when statistics page is ready for production!
    if app.config["ENV"] == "prod":
        return redirect("/")

    if not helper.logged_in():
        flash("Log in to use the application", "error")
        return redirect("/")

    submissions = survey_service.get_number_of_submissions_for_survey(survey_id)
    q_names_ids = helper.save_question_answer_charts(
        survey_service.get_answer_distribution_for_survey_questions(survey_id)
    )
    categories = survey_service.get_categories_of_survey(survey_id)

    users = survey_service.get_users_who_answered_survey(survey_id)
    # TODO: Remove this test data
    # users = [{"email": "userA@mail",
    #           "group_name": "A group",
    #           "answer_time": "15.9.2022 12:50:00"},
    #          {"email": "userB@mail",
    #           "group_name": "B group",
    #           "answer_time": "20.10.2022 14:50:00"}]
    users = users if users else []
    
    return render_template("surveys/statistics.html",
                           ENV=app.config["ENV"],
                           survey_id=survey_id,
                           submissions=submissions,
                           q_names_ids=q_names_ids,
                           users=users,
                           categories=categories)
