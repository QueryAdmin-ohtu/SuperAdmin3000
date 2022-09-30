# Architecture

## Backend

- Backend is implemented in Python 3 language
- Python Flask web framework is used 
- Flask uses Jinja template engine to produce frontend

### Directory structure

## Database

- Database used is PostgreSQL
- The backend uses SQLAlchemy toolkit to communicate with the database

## Frontend

- Simple HTML/CSS pages are displayed.

### TailwindCSS
This project uses TailwindCSS. To create a CSS file with the needed TailwindCSS utility classes install the [standalone TailwindCLI](https://tailwindcss.com/blog/standalone-cli). After insatllation run from the root of the project:
```
tailwindcss -c src/static/tailwind.config.js -i src/static/src/style.css -o src/static/css/main.css --watch
```
Tailwind now watches the HTML template files and creates a new css file when it is needed.


## Packaging
- The software is deployed as a Docker image

## Launching the application

Poetry Invoke mechanism is used. Available commands are defined in the `tasks.py` file.

## Environment variables

Following environment variables should be defined:

### `SECRET_KEY`

This is a 16 character hexadecimal string used by Flask session management. The key can be genrated from Python with token_hex method:

```
$ python3
>>> import secrets
>>> secrets.token_hex(16)
```

### `ENVIRONMENT`

Describes the platform software is running. When run on _localhost_, value should be:

```
ENVIRONMENT="local"
```

### `GOOGLE_CLIENT_ID`

Google Client ID for Google Single Sign On. The value of the variable is provided by Google.


