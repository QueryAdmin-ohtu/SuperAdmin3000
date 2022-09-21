from os import getenv
import secrets
from flask import Flask
from flask import render_template, redirect, session, request, abort
from google.oauth2 import id_token
from google.auth.transport import requests
from config import PORT

app = Flask(__name__)

app.secret_key = getenv("SECRET_KEY")
CLIENT_ID = getenv("GOOGLE_CLIENT_ID")

ENV=getenv("ENVIRONMENT")

match ENV:
    case 'local':
        print("ENV: local")
        GOOGLE_URI="http://localhost:5000/google_login"
    case 'test':
        print("ENV: test")
        GOOGLE_URI="TO BE DEFINED"
    case 'prod':
        print("ENV: prod")
        GOOGLE_URI="https://superadmin3000.herokuapp.com/google_login"

# TODO: Create a proper storage for the authorized users
authorized_google_accounts=["antti.vainikka36@gmail.com", "jatufin@gmail.com","me@juan.fi",
"niemi.leo@gmail.com", "oskar.sjolund93@gmail.com", "rami.piik@gmail.com", "siljaorvokki@gmail.com"]

@app.route("/", methods=["GET"])
def index():
    """ Main page

    If there's active session, index.html will be rendered,
    otherwise the login page will be displayed.
    """
    if _logged_in():
        return render_template("index.html", ENV=ENV)
    return render_template("google_login.html", URI=GOOGLE_URI, ENV=ENV)

@app.route("/google_login", methods=["POST"])
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
        token=request.form["credential"]
        if not token:
            abort(400, 'No token found.')
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID, clock_skew_in_seconds=10)
        email=idinfo['email']
        email_verified=idinfo['email_verified']
        if not email_verified:
            abort(400, 'Email not verified by Google.')
        first_name=idinfo['given_name']
        if _google_login_authorize(email):
            session["email"] = email
            session["username"]=first_name
            session["csrf_token"]=csrf_token_cookie
            return redirect("/")
    except ValueError:
        # Invalid token
        pass
    return "You are not authorized to use the service. Please contact your administrator."

def _google_login_authorize(email):
    """ Checks whether a Google account is authorized to access the app.
    """
    if email in authorized_google_accounts:
        return True
    return False

def _logged_in():
    """ Check if the session is active. This should be always used before
    rendering pages.
    """
    return "username" in session

def valid_token(form):
    """ Check if the token send with the form matches with the current
    session.
    """
    if not _logged_in():
        return False
    return form["csrf_token"] == session["csrf_token"]

@app.route("/logout", methods=["POST"])
def logout():
    """ Logout the user by removing all properties from the session
    and returning to the front page
    """
    _clear_session()
    return redirect("/")

@app.route("/new")
def new():
    """Renders the new questionnaire page
    """
    if not _logged_in():
        return redirect("/")

    return render_template("new.html", ENV=ENV)

@app.route("/edit")
def edit():
    """Renders the edit questionnaire page
    """
    if not _logged_in():
        return redirect("/")

    return render_template("edit.html", ENV=ENV)

@app.route("/test")
def test_page():
    """ The test page should only be shown if the user has logged in
    """
    if not _logged_in():
        abort(401)
    return render_template("test.html", ENV=ENV)

@app.route("/testform", methods=["POST"])
def test_form():
    """ All forms should include the hidden csrf_token field, so the
    session can be validated
    """

    if not _logged_in():
        abort(401)

    if not valid_token(request.form):
        abort(403)

    return render_template("testdata.html", testdata=request.form["testdata"], ENV=ENV)

def _clear_session():
    """ Logout the user and clear session properties
    """
    _remove_from_session("csrf_token")
    _remove_from_session("username")

def _remove_from_session(property_key):
    """ Checks if the given property name can be found in the session
    and removes it
    """
    if property_key in session:
        del session[property_key]

@app.route("/backdoor", methods=["GET"])
def backdoor_form():
    """ Form for logging in without Google
    """
    if ENV in ["local", "test"]:
        if _logged_in():
            return render_template("index.html", ENV=ENV)
        return render_template("backdoor_login.html", ENV=ENV)
    return abort(404)

@app.route("/backdoor", methods=["POST"])
def backdoor_login():
    """ Receive and process the backdoor login
    """
    if ENV in ["local", "test"]:
        username = request.form["username"]
        password = request.form["password"]

        if not _backdoor_validate_and_login(username, password):
            return abort(401)
    return abort(404)

def _backdoor_validate_and_login(username, password):
    """ Check if the given username password pair is correct
    If username and password match, a new session will be created
    """
    # TODO: Proper data storage for usernames and password hashes
    if username != "rudolf":
        return False
    if password != "secret":
        return False

    session["csrf_token"] = secrets.token_hex(16)
    session["username"] = username
    return True

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=PORT)
