from flask import render_template, redirect, request, abort, Blueprint, flash
from flask import current_app as app

from google.oauth2 import id_token
from google.auth.transport import requests

import helper
from logger.logger import Logger

from services.survey_service import survey_service

home = Blueprint("home", __name__)


@home.route("/", methods=["GET"])
def index():
    """Main page
    If there's an active session, main page with existing surveys
    will be rendered, otherwise the login page will be displayed.
    """
    if not helper.logged_in():
        return render_template("home/google_login.html",
                               URI=app.config["GOOGLE_URI"],
                               ENV=app.config["ENV"])

    surveys = survey_service.get_all_surveys()

    if surveys is False:
        report = "There are no surveys"
        return render_template("index.html",
                               no_surveys=report,
                               ENV=app.config["ENV"])

    return render_template("home/index.html",
                           surveys=surveys,
                           ENV=app.config["ENV"])


@home.route("/google_login", methods=["POST"])
def google_login():
    """ Login with a Google account.
    """
    try:
        csrf_token_cookie = request.cookies.get('g_csrf_token')
        if not csrf_token_cookie:
            abort(400, 'No CSRF token in Cookie.')

        csrf_token_body = request.form['g_csrf_token']
        if not csrf_token_body:
            abort(400, 'No CSRF token in post body.')

        if csrf_token_cookie != csrf_token_body:
            abort(400, 'Failed to verify double submit cookie.')

        token = request.form["credential"]
        if not token:
            abort(400, 'No token found.')

        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), app.config["CLIENT_ID"], clock_skew_in_seconds=10)
        email = idinfo['email']

        email_verified = idinfo['email_verified']
        if not email_verified:
            abort(400, 'Email not verified by Google.')

        first_name = idinfo['given_name']
        if survey_service.check_if_authorized_google_login(email):
            helper.update_session(email, first_name, csrf_token_cookie)
            return redirect("/")

    except ValueError:
        # Invalid token
        pass

    flash("You are not authorized to use the service. Please contact your administrator.", "error")
    return redirect("/")


@home.route("/logout", methods=["POST"])
def logout():
    """ Logout the user by removing all properties from the session
    and returning to the front page
    """
    if not helper.valid_token(request.form):
        abort(403)

    helper.clear_session()

    return redirect("/")


@home.route("/backdoor", methods=["GET"])
def backdoor_form():
    """ Form for logging in without Google
    """
    if app.config["ENV"] not in ["prod"]:
        if helper.logged_in():
            return render_template("home/index.html", ENV=app.config["ENV"])
        return render_template("home/backdoor_login.html", ENV=app.config["ENV"])
    return abort(404)


@home.route("/backdoor", methods=["POST"])
def backdoor_login():
    """ Receive and process the backdoor login

    Session token is not validated in this POST handler,
    because there should be no no active session yet.

    THIS BACKDOOR WILL BE REMOVED FROM THE PRODUCTION CODE
    """
    if app.config["ENV"] not in ["prod"]:
        username = request.form["username"]
        password = request.form["password"]
        if not helper.backdoor_validate_and_login(username, password):
            return abort(401)
    return redirect("/")


@home.route("/admins", methods=["GET"])
def list_admins():
    """ Returns the page with list of admins """
    if not helper.logged_in():
        flash("Log in to use the application", "error")
        return redirect("/")

    admins = survey_service.get_all_admins()
    return render_template("home/list_admins.html", admins=admins, ENV=app.config["ENV"])


@home.route("/admins/new", methods=["POST"])
def new_admin():
    """ Adds an authorized user to the application """
    if not helper.valid_token(request.form):
        abort(403)
    email = request.form["email"]
    survey_service.add_admin(email)

    return redirect("/admins")


@home.route("/ping")
def ping():
    """ Test function for general testing
    """
    return "pong"


@home.before_request
def before_request():
    """Save requests to the log"""
    user = helper.current_user()
    Logger(user).log_post_request(request)
