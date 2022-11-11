import datetime

from flask import render_template, redirect, request, Blueprint, flash, abort
from flask import current_app as app
import helper
from services.survey_service import survey_service

stats = Blueprint("stats", __name__)

timeformat = "%d.%m.%Y %H:%M"

@stats.route("/surveys/<survey_id>/statistics", methods=["GET"])
def statistics(survey_id):
    """Shows the statistics for the specific survey"""

    submissions = survey_service.get_number_of_submissions_for_survey(
        survey_id)
    categories = survey_service.calculate_average_scores_by_category(survey_id)

    users = survey_service.get_users_who_answered_survey(survey_id)

    users = users if users else []
    total_users = len(users)

    group_names = {"All user groups": ""}
    for user in users:
        group_names[user.group_name] = user.group_name

    answer_distribution = helper.save_question_answer_charts(
        survey_service.get_answer_distribution_for_survey_questions(survey_id)
    )

    filter_start_date = (datetime.datetime.now() - datetime.timedelta(days=10*365)).strftime(timeformat)
    filter_end_date = datetime.datetime.now().strftime(timeformat)
    filter_group_name = ""
    filter_email = ""

    return render_template("surveys/statistics.html",
                           ENV=app.config["ENV"],
                           survey_id=survey_id,
                           submissions=submissions,
                           users=users,
                           total_users=total_users,
                           categories=categories,
                           answer_distribution=answer_distribution,
                           filter_start_date=filter_start_date,
                           filter_end_date=filter_end_date,
                           filter_group_name=filter_group_name,
                           filter_email=filter_email,
                           group_names=group_names,
                           show_userlist=False
    )

@stats.route("/surveys/<survey_id>/statistics/filter", methods=["POST"])
def filtered_statistics(survey_id):
    """Shows the statistics for the specific survey and filtered
    set of users
    """
    if app.config["ENV"] == "prod":
        return redirect("/")

    try:
        filter_start_date = datetime.datetime.strptime(request.form["filter_start_date"], timeformat)
        filter_end_date = datetime.datetime.strptime(request.form["filter_end_date"], timeformat)
    except ValueError:
        return redirect(f"/surveys/{survey_id}/statistics")

    filter_group_name = request.form["filter_group_name"]
    filter_email = request.form["filter_email"]

    submissions = survey_service.get_number_of_submissions_for_survey(survey_id)
    answer_distribution = helper.save_question_answer_charts(
        survey_service.get_answer_distribution_for_survey_questions(survey_id,
                                                                    filter_start_date,
                                                                    filter_end_date,
                                                                    filter_group_name,
                                                                    filter_email),
        filter_group_name
    )
    categories = survey_service.get_categories_of_survey(survey_id)

    users = survey_service.get_users_who_answered_survey(survey_id)
    users = users if users else []
    total_users = len(users)

    group_names = {"All user groups": ""}
    for user in users:
        group_names[user.group_name] = user.group_name

    users = survey_service.get_users_who_answered_survey_filtered(survey_id,
                                                                  filter_start_date,
                                                                  filter_end_date,
                                                                  filter_group_name,
                                                                  filter_email)

    users = users if users else []

    filter_start_date = filter_start_date.strftime(timeformat)
    filter_end_date = filter_end_date.strftime(timeformat)


    return render_template("surveys/statistics.html",
                           ENV=app.config["ENV"],
                           survey_id=survey_id,
                           submissions=submissions,
                           answer_distribution=answer_distribution,
                           users=users,
                           total_users=total_users,
                           categories=categories,
                           filter_start_date=filter_start_date,
                           filter_end_date=filter_end_date,
                           filter_group_name=filter_group_name,
                           filter_email=filter_email,
                           group_names=group_names,
                           show_userlist=True)


@stats.before_request
def before_request():
    """Check session status"""
    if not helper.logged_in():
        flash("Log in to use the application", "error")
        return redirect("/")

    if request.method == "POST" and not helper.valid_token(request.form):
        abort(400, 'Invalid CSRF token')
