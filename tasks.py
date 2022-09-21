from invoke import task

@task
def start_local(ctx):
    ctx.run("export FLASK_env='local' && python3 src/app.py")

@task
def start_test(ctx):
    ctx.run("export FLASK_env='test' && python3 src/app.py")

@task
def start_prod(ctx):
    ctx.run("export FLASK_env='prod' && python3 src/app.py")

@task
def start(ctx):
    ctx.run("python3 src/app.py")

@task
def lint(ctx):
    ctx.run("pylint src")

@task
def tests(ctx):
    ctx.run("pytest")

@task
def e2etests(ctx):
    ctx.run("robot src/tests/robot_tests/")

@task
def format(ctx):
    ctx.run("autopep8 --in-place --recursive src")

@task
def tailwindcss(ctx):
    ctx.run("tailwindcss -c src/static/tailwind.config.js -i src/static/src/style.css -o src/static/css/main.css --watch")