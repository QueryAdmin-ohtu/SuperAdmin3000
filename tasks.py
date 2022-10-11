from invoke import task


@task
def start(ctx):
    ctx.run("python3 src/app.py")

@task
def lint(ctx):
    ctx.run("pylint --fail-under=9 src")

@task
def tests(ctx):
    ctx.run("pytest")

@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest")

@task
def coveragehtml(ctx):
    ctx.run("coverage html")

@task
def coveragexml(ctx):
    ctx.run("coverage xml")
    
@task
def e2etests(ctx):
    ctx.run("robot src/tests/robot_tests/")

@task
def e2etestsheroku(ctx):
    ctx.run("robot -v URL:https://test-superadmin3000.herokuapp.com/ src/tests/robot_tests/")

@task
def format(ctx):
    ctx.run("autopep8 --in-place --recursive src")

@task
def tailwindcss(ctx):
    ctx.run("tailwindcss -c src/static/tailwind.config.js -i src/static/src/style.css -o src/static/css/main.css --watch")

@task
def init_db(ctx, db):
    beginning1="psql -d"
    end1="-c 'drop table if exists \"Admins\", \"Categories\", \"Category_results\", \"Industries\", \"Organizations\", \"Question_answers\",   \"Questions\", \"Survey_results\", \"Survey_user_groups\", \"Surveys\", \"User_answers\", \"Users\" cascade;'"
    drop_tables=' '.join([beginning1,db,end1])
    ctx.run(drop_tables)

    beginning2="psql -d"
    end2="-f schema.sql"
    create_tables=' '.join([beginning2,db,end2])
    ctx.run(create_tables)

    beginning3="psql"
    end3="-Atq -f reset.sql -o temp"
    update_sequences=' '.join([beginning3,db,end3])
    ctx.run(update_sequences)

    beginning4="psql"
    end4="-f temp"
    clean=' '.join([beginning4,db,end4])
    ctx.run(clean)
    ctx.run("rm temp")