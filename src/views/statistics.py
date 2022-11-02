from flask import render_template, redirect, Blueprint, flash
from flask import current_app as app
import helper
from services.survey_service import survey_service

stats = Blueprint("stats", __name__)


@stats.route("/surveys/<survey_id>/statistics", methods=["GET"])
def statistics(survey_id):
    """Shows the statistics for the specific survey"""

    if not helper.logged_in():
        flash("Log in to use the application", "error")
        return redirect("/")

    submissions = survey_service.get_number_of_submissions_for_survey(
        survey_id)
    answer_distribution = survey_service.get_answer_distribution_for_survey_questions(
        survey_id)

    return render_template("surveys/statistics.html",
                           ENV=app.config["ENV"],
                           survey_id=survey_id,
                           submissions=submissions,
                           answer_distribution=answer_distribution)
