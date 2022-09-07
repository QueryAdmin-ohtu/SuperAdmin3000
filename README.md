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

## Running unit tests

From `poetry shell` run:
```
$ pytest
```

## Instructions/resources/support for developers
- Poetry quick guide from the [Ohjelmistotekniikka](https://ohjelmistotekniikka-hy.github.io/python/viikko2#poetry-ja-riippuvuuksien-hallinta) course
- Flask and PostGreSQL material from the [Tietokantasovellus](https://hy-tsoha.github.io/materiaali/osa-1/#johdatus-web-sovelluksiin) course
