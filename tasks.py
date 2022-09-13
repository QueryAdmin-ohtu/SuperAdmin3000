from invoke import task

@task
def start(ctx):
    ctx.run("cd src; flask run")

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