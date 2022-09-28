from flask import render_template, redirect, request, abort
from google.oauth2 import id_token
from google.auth.transport import requests
from app import app, CLIENT_ID, ENV, db
import helper
import db_queries as queries

if ENV == 'local':
    print("ENV: local")
    GOOGLE_URI = "http://localhost:5000/google_login"
elif ENV == 'test':
    print("ENV: test")
    GOOGLE_URI = "TO BE DEFINED"
elif ENV == 'prod':
    print("ENV: prod")
    GOOGLE_URI = "https://superadmin3000.herokuapp.com/google_login"
else:
    print("ENV:", ENV)  # Should this throw an error?


@app.route("/testdb/new")
def new_message():
    """  Create new message to test database
    """
    return render_template("testdb_new.html", ENV=ENV)


@app.route("/testdb/add_question", methods=["POST"])
def send_message():
    """ Add a question to the database
    """
    question = request.form["content"]

    # pylint: disable-next=line-too-long
    sql = "INSERT INTO \"Questions\" (\"text\", \"surveyId\", \"createdAt\", \"updatedAt\") VALUES (:question, '1', (select CURRENT_TIMESTAMP), (select CURRENT_TIMESTAMP))"
    db.session.execute(sql, {"question": question})
    db.session.commit()

    return redirect("/testdb")


@app.route("/testdb")
def testdb():
    """ Open the test database
    """
    result = db.session.execute("SELECT text FROM \"Questions\"")
    questions = result.fetchall()
    return render_template("testdb.html", count=len(questions), questions=questions, ENV=ENV)


@app.route("/", methods=["GET"])
def index():
    """ Main page

    If there's active session, index.html will be rendered,
    otherwise the login page will be displayed.
    """
    if helper.logged_in():
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
        token = request.form["credential"]
        if not token:
            abort(400, 'No token found.')
        idinfo = id_token.verify_oauth2_token(
            token, requests.Request(), CLIENT_ID, clock_skew_in_seconds=10)
        email = idinfo['email']
        email_verified = idinfo['email_verified']
        if not email_verified:
            abort(400, 'Email not verified by Google.')
        first_name = idinfo['given_name']
        if queries.google_login_authorize(email):
            helper.update_session(email, first_name, csrf_token_cookie)
            return redirect("/")
    except ValueError:
        # Invalid token
        pass
    return "You are not authorized to use the service. Please contact your administrator."


@app.route("/logout", methods=["POST"])
def logout():
    """ Logout the user by removing all properties from the session
    and returning to the front page
    """
    helper.clear_session()
    return redirect("/")


@app.route("/new")
def new():
    """Renders the new questionnaire page
    """
    if not helper.logged_in():
        return redirect("/")

    return render_template("new.html", ENV=ENV)


@app.route("/edit")
def edit():
    """Renders the edit questionnaire page
    """
    if not helper.logged_in():
        return redirect("/")

    return render_template("edit.html", ENV=ENV)


@app.route("/test")
def test_page():
    """ The test page should only be shown if the user has logged in
    """
    if not helper.logged_in():
        abort(401)
    return render_template("test.html", ENV=ENV)


@app.route("/testform", methods=["POST"])
def test_form():
    """ All forms should include the hidden csrf_token field, so the
    session can be validated
    """

    if not helper.logged_in():
        abort(401)

    if not helper.valid_token(request.form):
        abort(403)

    return render_template("testdata.html", testdata=request.form["testdata"], ENV=ENV)


@app.route("/backdoor", methods=["GET"])
def backdoor_form():
    """ Form for logging in without Google
    """
    if ENV not in ["prod"]:
        if helper.logged_in():
            return render_template("index.html", ENV=ENV)
        return render_template("backdoor_login.html", ENV=ENV)
    return abort(404)


@app.route("/backdoor", methods=["POST"])
def backdoor_login():
    """ Receive and process the backdoor login
    """
    if ENV not in ["prod"]:
        username = request.form["username"]
        password = request.form["password"]
        if not helper.backdoor_validate_and_login(username, password):
            return abort(401)
    return redirect("/")


@app.route("/ping")
def ping():
    """ Test function for general testing
    """
    return "pong"