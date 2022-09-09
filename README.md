# SuperAdmin3000
## Starting the application
- Activate poetry environment: `poetry install`
- Start flask: `poetry run flask run`
- Or start Poetry shell first and run Flask from within the environment:
```
$ poetry shell
$ flask run
```
- Go to http://127.0.0.1:5000/

## Tests
### End-to-End
RobotFramework End-to-End tests can be run by starting the server and running:
```
$ poetry shell
$ robot tests/robot_tests/
```
These tests require ChromeDriver. Instructions on installation [here](https://ohjelmistotuotanto-hy.github.io/chromedriver_asennusohjeet/).

### Unit

From `poetry shell` run:
```
$ pytest
```
To gather test coverage staistics, run the following command inside poetry shell:
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
