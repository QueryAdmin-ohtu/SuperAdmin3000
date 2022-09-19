from invoke import task

@task
def start(ctx):
    ctx.run("cd src; flask run --host=0.0.0.0")

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