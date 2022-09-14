from flask import Flask
from flask import render_template, redirect, session, request, abort

from os import getenv

import secrets


app = Flask(__name__)

app.secret_key = "ffobar" #getenv("SECRET_KEY")

@app.route("/")
def index():
    """ Main page

    If there's active session, index.html will be rendered,
    otherwise the login page will be displaye.
    """
    if _logged_in():
        return render_template("index.html")
    else:
        return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    """ Receive and process the login form
    """
    username = request.form["username"]
    password = request.form["password"]

    if not _validate_and_login(username, password):
        return abort(401)
        
    return redirect("/")

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
        abort(401)

    return render_template("new.html")

@app.route("/edit")
def edit():
    """Renders the edit questionnaire page
    """
    if not _logged_in():
        abort(401)

    return render_template("edit.html")
        
@app.route("/test")
def test_page():
    """ The test page should only be shown if the user has logged in
    """
    if not _logged_in():
        abort(401)
        
    return render_template("test.html")

@app.route("/testform", methods=["POST"])
def test_form():
    """ All forms should include the hidden csrf_token field, so the
    session can be validated
    """

    if not _logged_in():
        abort(401)

    if not _valid_token(request.form):
        abort(403)

    return render_template("testdata.html", testdata=request.form["testdata"])
    
def _validate_and_login(username, password):
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

def _valid_token(form):
    """ Check if the token send with the form matches with the current
    session.
    """
    if not _logged_in():
        return False

    return form["csrf_token"] == session["csrf_token"]

def _clear_session():
    """ Logout the user and clear session properties
    """
    _remove_from_session("csrf_token")
    _remove_from_session("username")    

def _remove_from_session(property):
    """ Checks if the given property name can be found in the session
    and removes it
    """
    if property in session:
        del session[property]

def _logged_in():
    """ Check if the session is active. This should be always used before
    rendering pages.
    """
    return "username" in session
        
