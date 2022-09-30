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
- Github builds a Docker image
- The docker image is pushed to Heroku
- There are two Heroku environments: One for testing and one for product deployment
- The process goes ass follows:

1. A developer runs all tests locally
1. The developer pushes pull request to Github. The branch name starts with "dev_"
1. Github runs style and quality checks (Lint)
1. Github runs unit tests
1. Github builds Docker image
1. Githup deploys the image to Heroku
1. Heroku runs E2E tests (Robot framework)
1. Heroku return test results to Github
1. Pull request is accepted and merged manually to the main branch
1. Github builds the docker image in main branch
1. Githup deploys the image to Heroku


## Docker
The preliminary docker image can be built with
````
$ (sudo) docker build . -t superadmin3000
````

To run the container locally:
````
 $ (sudo) docker run -p 3000:5000 superadmin

````
When the container is succesfully running the application can be accessed at [http://localhost:3000](http://localhost:3000)
