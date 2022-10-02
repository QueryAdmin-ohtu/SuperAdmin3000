from datetime import datetime
from app import db


def authorized_google_login(email):
    """ Checks whether a Google account is authorized to access the app.
    """
    sql = "SELECT id FROM \"Admins\" WHERE email=:email"
    result = db.session.execute(sql, {"email": email})

    user = result.fetchone()

    if user:
        return True

    return False


def create_survey(name, title, survey):
    """ Inserts a survey to table Surveys based
    on given parameters and returns the id """
    created = datetime.now()
    sql = """
    INSERT INTO "Surveys"
    (name,"createdAt","updatedAt",title_text,survey_text)
    VALUES (:name, :createdAt, :updatedAt, :title_text, :survey_text)
    RETURNING id """
    values = {
        "name": name,
        "createdAt": created,
        "updatedAt": created,
        "title_text": title,
        "survey_text": survey
    }
    survey_id = db.session.execute(sql,values).fetchone()
    db.session.commit()
    return survey_id[0]

def get_survey(survey_id):
    """ Looks up survey information with
    id and returns it in a list"""
    sql = """ SELECT * FROM "Surveys" WHERE id=:id """
    survey = db.session.execute(sql,{"id":survey_id}).fetchone()
    if not survey:
        return False
    return survey


def get_questions_of_questionnaire(questionnaire_id):
    """ Fetches questions of a given questionnaire
    Args:
      questionnaire_id: Id of the questionnaire

    Returns:
      An array containing each question object
    """
    sql = "SELECT * FROM \"Questions\" WHERE \"Questions\".\"surveyId\"=:questionnaire_id"
    result = db.session.execute(sql, {"questionnaire_id": questionnaire_id})

    questions = result.fetchall()

    return questions
