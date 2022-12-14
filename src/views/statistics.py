import datetime
import uuid

from flask import render_template, redirect, request, Blueprint, flash, abort
from flask import current_app as app
import helper
from services.statistic_service import statistic_service
from services.survey_service import survey_service

stats = Blueprint("stats", __name__)

TIMEFORMAT = "%d.%m.%Y %H:%M"
HTML_DATE_INPUT_TIMEFORMAT = "%Y-%m-%dT%H:%M"


@stats.route("/surveys/<survey_id>/statistics", methods=["GET"])
def statistics(survey_id):
    """Shows the statistics for the specific survey"""

    survey = survey_service.get_survey(survey_id)
    submissions = statistic_service.get_number_of_submissions_for_survey(
        survey_id)
    categories = statistic_service.calculate_average_scores_by_category(survey_id)

    users = statistic_service.get_users_who_answered_survey(survey_id)

    users = users if users else []
    total_users = len(users)

    group_names = {"All": "All user groups"}
    for user in users:
        group_names[user.group_id] = user.group_name

    answer_distribution = statistic_service.get_answer_distribution_for_survey_questions(
        survey_id)

    answer_charts = helper.save_question_answer_charts(
        answer_distribution
    )

    filter_start_date = (datetime.datetime.now() -
                         datetime.timedelta(days=10*365)).strftime(HTML_DATE_INPUT_TIMEFORMAT)
    filter_end_date = datetime.datetime.now().strftime(HTML_DATE_INPUT_TIMEFORMAT)
    filter_email = ""

    return render_template("surveys/statistics.html",
                           ENV=app.config["ENV"],
                           survey=survey,
                           survey_id=survey_id,
                           submissions=submissions,
                           users=users,
                           total_users=total_users,
                           categories=categories,
                           answer_charts=answer_charts,
                           filter_start_date=filter_start_date,
                           filter_end_date=filter_end_date,
                           filter_group_id="",
                           filter_email=filter_email,
                           group_names=group_names,
                           show_userlist=False,
                           filtered=False)


@stats.route("/surveys/<survey_id>/statistics/filter", methods=["POST"])
def filtered_statistics(survey_id):
    """Shows the statistics for the specific survey and filtered
    set of users
    """
    try:
        filter_start_date = datetime.datetime.strptime(
            request.form["filter_start_date"], HTML_DATE_INPUT_TIMEFORMAT)
        filter_end_date = datetime.datetime.strptime(
            request.form["filter_end_date"], HTML_DATE_INPUT_TIMEFORMAT)
    except ValueError:
        print("Value error!")
        return redirect(f"/surveys/{survey_id}/statistics")

    survey = survey_service.get_survey(survey_id)

    filter_group_id = request.form["filter_group_id"]
    filter_email = request.form["filter_email"]

    if filter_group_id == "All":
        filter_group_id = None
    else:
        filter_group_id = uuid.UUID(filter_group_id)

    # submissions = survey_service.get_number_of_submissions_for_survey(
    #     survey_id)

    users = statistic_service.get_users_who_answered_survey(survey_id)
    users = users if users else []
    total_users = len(users)

    group_names = {"All": "All user groups"}
    for user in users:
        group_names[user.group_id] = user.group_name

    filter_group_name = group_names[filter_group_id]

    answer_distribution = statistic_service.get_answer_distribution_for_survey_questions(survey_id,
                                                                                      filter_start_date,
                                                                                      filter_end_date,
                                                                                      filter_group_id,
                                                                                      filter_email)
    answer_charts = helper.save_question_answer_charts(
        answer_distribution,
        filter_group_name,
        filter_start_date,
        filter_end_date
    )

    categories = statistic_service.calculate_average_scores_by_category(survey_id,
                                                                     filter_group_id,
                                                                     filter_start_date,
                                                                     filter_end_date,
                                                                     filter_email)

    users = statistic_service.get_users_who_answered_survey_filtered(survey_id,
                                                                  filter_start_date,
                                                                  filter_end_date,
                                                                  filter_group_id,
                                                                  filter_email)

    users = users if users else []

    filter_start_date = filter_start_date.strftime(HTML_DATE_INPUT_TIMEFORMAT)
    filter_end_date = filter_end_date.strftime(HTML_DATE_INPUT_TIMEFORMAT)

    if not filter_group_id:
        filter_group_id = "All"

    return render_template("surveys/statistics.html",
                           ENV=app.config["ENV"],
                           survey=survey,
                           survey_id=survey_id,
                           answer_charts=answer_charts,
                           users=users,
                           total_users=total_users,
                           categories=categories,
                           filter_start_date=filter_start_date,
                           filter_end_date=filter_end_date,
                           filter_group_id=filter_group_id,
                           filter_group_name=filter_group_name,
                           filter_email=filter_email,
                           group_names=group_names,
                           show_userlist=True,
                           filtered=True)


@stats.before_request
def before_request():
    """Check session status"""
    if not helper.logged_in():
        flash("Log in to use the application", "error")
        return redirect("/")

    if request.method == "POST" and not helper.valid_token(request.form):
        abort(400, 'Invalid CSRF token')
