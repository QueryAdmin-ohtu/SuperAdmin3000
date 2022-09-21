# Deploying the software

## Simplest way to launch the application
- Activate poetry environment: `poetry install`
- Start flask: `poetry run invoke start`
- Or start Poetry shell first and run Flask from within the environment:
```
$ poetry shell
$ invoke start
```

### Dependency management

- Poetry is used to manage and install dependencies
- The `pyproject.toml` file contains project requirements
- Other systems, such as PIP, should be avoided during the development to avoid conflicts

### PIP dependencies

For environments which don't support Poetry, (such as Heroku) the PIP dependency `requirements.txt` file can be generated manually from `pyproject.toml` file by running following comand inside Poetry shell:
```
pip list --format freeze > requirements.txt
```
## Continuous Integration

- Github Actions has been used for CI/CP pipeline
- The process goes ass follows:

1. A developer runs all tests locally
1. The developer pushes pull request to Github
1. Github runs style and quality checks (Lint)
1. Github runs unit tests
1. Github runs end-to-end-tests
1. Github build Docker image
1. Pull request is accepted and merged
1. Github pushes the docker image to the server (Heroku)

As from the above can be seen, the Docker image is deployed to the server only after a main branch push/merge. Only tests are run for pull requests.
