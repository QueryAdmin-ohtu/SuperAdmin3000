from db import db


class SurveyRepository:
    """
    A class for interacting with the survey database
    """

    def __init__(self, db_connection=db):
        self.db_connection = db_connection

    def authorized_google_login(self, email):
        """ Checks whether a Google account is authorized to access the app.
        """
        sql = "SELECT id FROM \"Admins\" WHERE email=:email"
        result = self.db_connection.session.execute(sql, {"email": email})

        user = result.fetchone()

        if user:
            return True

        return False

    def create_survey(self, name, title, survey, created):
        """ Inserts a survey to table Surveys based
        on given parameters and returns the id """
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
        survey_id = self.db_connection.session.execute(sql, values).fetchone()
        self.db_connection.session.commit()
        return survey_id[0]

    def create_question(self, text, survey_id, category_weights, created):
        """ Inserts a new question to table Questions based
        on given parameters and returns the id """
        sql = """
        INSERT INTO "Questions"
        ("text", "surveyId", "category_weights", "createdAt","updatedAt")
        VALUES (:text, :survey_id, :category_weights, :createdAt, :updatedAt)
        RETURNING id """
        values = {
            "text": text,
            "survey_id": survey_id,
            "category_weights": category_weights,
            "createdAt": created,
            "updatedAt": created
        }
        survey_id = db.session.execute(sql, values).fetchone()
        db.session.commit()
        return survey_id[0]

    def get_survey(self, survey_id):
        """ Looks up survey information with
        id and returns it in a list"""
        sql = """ SELECT * FROM "Surveys" WHERE id=:id """
        survey = self.db_connection.session.execute(
            sql, {"id": survey_id}).fetchone()
        if not survey:
            return False
        return survey

    def get_all_surveys(self):
        """ Fetches all surveys, counts the questions
        for each survey and the amount of submissions
        related to the survey returning a list

        Returns: Array containing the survey id, title,
        question count and submission count """
        sql = """
        SELECT 
            s.id, 
            s.title_text,
            COUNT(DISTINCT q.id) AS questions,
            COUNT(DISTINCT r.id) AS submissions
        FROM "Surveys" AS s
        LEFT JOIN "Survey_results" AS r
            ON s.id = r."surveyId"
        LEFT JOIN "Questions" AS q
            ON s.id = q."surveyId"
        GROUP BY s.id
        """
        surveys = self.db_connection.session.execute(sql).fetchall()

        if not surveys:
            return False
        return surveys

    def get_questions_of_survey(self, survey_id):
        """ Fetches questions of a given survey
        Args:
          survey_id: Id of the survey

        Returns:
          An array containing each question object
        """
        sql = "SELECT * FROM \"Questions\" WHERE \"Questions\".\"surveyId\"=:survey_id"
        result = self.db_connection.session.execute(
            sql, {"survey_id": survey_id})

        questions = result.fetchall()

        return questions

    def get_all_categories(self):
        """ Fetches all categories from the database

        Returns:
        An array containing survey id's, names and titles
        """
        sql = """ SELECT id, name, description, content_links FROM "Categories" """
        result = self.db_connection.session.execute(sql)

        categories = result.fetchall()

        return categories

    def get_all_questions(self):
        """ Fetches texts of all questions from the database

        Returns:
        An array containing question texts
        """
        sql = """ SELECT text FROM "Questions" """
        result = self.db_connection.session.execute(sql)

        questions = result.fetchall()

        return questions
