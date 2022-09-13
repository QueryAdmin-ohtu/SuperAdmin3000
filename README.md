# SuperAdmin3000
## Starting the application
- Activate poetry environment: `poetry install`
- Start flask: `poetry run invoke start`
- Or start Poetry shell first and run Flask from within the environment:
```
$ poetry shell
$ invoke start
```
- Go to http://127.0.0.1:5000/

## Tests
### End-to-End
RobotFramework End-to-End tests can be run by starting the server and running:
```
$ poetry shell
$ invoke e2etests
```
These tests require ChromeDriver. Instructions on installation [here](https://ohjelmistotuotanto-hy.github.io/chromedriver_asennusohjeet/).

### Unit

From `poetry shell` run:
```
$ invoke tests
```
To gather test coverage statistics, run the following command inside poetry shell:
```
$ coverage run --branch -m pytest
```
The coverage report can be shown on command line with:
```
$ coverage report -m
```
A HTML report will be created to `htmlcov` subdirectory with command: (this can be viewed by opening the `index.html` file in a browser)
```
$ coverage html
```

## Instructions/resources/support for developers
- Poetry quick guide from the [Ohjelmistotekniikka](https://ohjelmistotekniikka-hy.github.io/python/viikko2#poetry-ja-riippuvuuksien-hallinta) course
- Flask and PostGreSQL material from the [Tietokantasovellus](https://hy-tsoha.github.io/materiaali/osa-1/#johdatus-web-sovelluksiin) course

## Definition of done

The definition of done for sprint 1 or until the minimum viable product (MVP) has been developed is as follows:
- The source code is peer reviewed and linted
- The source code is deployed onto the ‘master’ branch 
- The source code is unit tested with a code coverage of 70%

Sprint 2 / MVP onwards:

Every developer commits to creating unit tests and E2E-tests using robot framework (when applicable) before deployment. Also all code submitted to the main branch should be peer reviewed utilising pull requests. The automated tests should reach a code coverage of 75%

## Login and session control

The secret key is stored to an environment variable `SECRET KEY`

Username and session token are store in Flask `session` dictionary.

In route functions the existence of current session should be checked before returning the page to user. If there's no current session, an abort error could be given, or a different page returned. A specified function `_logged_in()`exists for this.

Example:
```
@app.route("/test")
def test_page():
    """ The test page should only be shown if the user has logged in
    """
    if not _logged_in():
        abort(401)
        
    return render_template("test.html")
```

Every form should include hidden field containing the session token, so the route can compare it to the valid token:

Token in the template file:
```
<form action="/testform" method="POST">
  <input type="hidden" name="csrf_token" value="{{ session.csrf_token }}">
  Some data: <input type="text" name="testdata">
  <input type="submit" value="Submit">
</form>
```

And in the route:
```
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
```

During logout, the `_clear_session()` function should be called, which removes username and token variables from the session dictionary.
