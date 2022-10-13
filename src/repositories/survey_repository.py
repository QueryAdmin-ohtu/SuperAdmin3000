from datetime import time
from sqlalchemy import exc

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

    def create_survey(self, name, title, survey):
        """ Inserts a survey to table Surveys based
        on given parameters and returns the id """
        sql = """
        INSERT INTO "Surveys"
        (name,"createdAt","updatedAt",title_text,survey_text)
        VALUES (:name, NOW(), NOW(), :title_text, :survey_text)
        RETURNING id """
        values = {
            "name": name,
            "title_text": title,
            "survey_text": survey
        }

        try:
            survey_id = self.db_connection.session.execute(
                sql, values).fetchone()
            self.db_connection.session.commit()
        except exc.SQLAlchemyError:
            return None

        return survey_id[0]

    def create_question(self, text, survey_id, category_weights):
        """ Inserts a new question to table Questions based
        on given parameters.

        Returns:
            Id of the new question. """
        sql = """
        INSERT INTO "Questions"
        ("text", "surveyId", "category_weights", "createdAt","updatedAt")
        VALUES (:text, :survey_id, :category_weights, NOW(), NOW())
        RETURNING id """
        values = {
            "text": text,
            "survey_id": survey_id,
            "category_weights": category_weights
        }
        question_id = db.session.execute(sql, values).fetchone()
        db.session.commit()
        return question_id[0]

    def create_answer(self, text, points, question_id):
        """ Inserts a new answer to table Question_answers based
        on given parameters.

        Returns:
            Id of the new answer """
        sql = """
        INSERT INTO "Question_answers"
        ("text", "points", "questionId", "createdAt","updatedAt")
        VALUES (:text, :points, :question_id, NOW(), NOW())
        RETURNING id """
        values = {
            "text": text,
            "points": points,
            "question_id": question_id
        }
        answer_id = db.session.execute(sql, values).fetchone()
        db.session.commit()
        return answer_id[0]

    def update_question(self, question_id, text, category_weights):
        """ Updates a question from the table Questions
        based on given parameters. If text nor category
        weights have been changed, nothing will happen
        and False will be returned. Otherwise, changes
        will take place and True is returned """
        original = self.get_question(question_id)
        sql = """ UPDATE "Questions" SET "updatedAt"=NOW()
        WHERE id=:question_id """
        sql2 = False
        sql3 = False

        if text != original[0]:
            sql2 = """ UPDATE "Questions" SET text=:text
            WHERE id=:question_id """
            self.db_connection.session.execute(
                sql2, {"text": text, "question_id": question_id})

        if category_weights != original[3]:
            sql3 = """ UPDATE "Questions" SET category_weights=:category_weights
            WHERE id=:question_id """
            self.db_connection.session.execute(
                sql3, {"category_weights": category_weights, "question_id": question_id})

        if sql2 or sql3:
            self.db_connection.session.execute(
                sql, {"question_id": question_id})
            self.db_connection.session.commit()

        return sql2 or sql3

    def delete_survey(self, survey_id):
        """ Deletes a survey from Surveys after deleting all
        questions, results and groups which relate to it.
        After deletion, checks if survey has been deleted
        and returns the result """
        sql = """ DELETE FROM "Questions" WHERE "surveyId"=:id """
        db.session.execute(sql, {"id": survey_id})
        sql = """ DELETE FROM "Survey_results" WHERE "surveyId"=:id """
        db.session.execute(sql, {"id": survey_id})
        sql = """ DELETE FROM "Survey_user_groups" WHERE "surveyId"=:id """
        db.session.execute(sql, {"id": survey_id})
        sql = """ DELETE FROM "Surveys" WHERE "id"=:id """
        db.session.execute(sql, {"id": survey_id})
        db.session.commit()
        if self.get_survey(survey_id) is False:
            return True
        return False

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
        sql = "SELECT * FROM \"Questions\" WHERE \"Questions\".\"surveyId\"=:survey_id ORDER BY id"
        result = self.db_connection.session.execute(
            sql, {"survey_id": survey_id})

        questions = result.fetchall()

        return questions

    def get_all_categories(self):
        """ Fetches all categories from the database.

        Returns:
        An array containing id, name, description, content_links of each category.
        """
        sql = """ SELECT id, name, description, content_links FROM "Categories" """
        result = self.db_connection.session.execute(sql)

        categories = result.fetchall()

        return categories

    def delete_question_from_survey(self, question_id):
        """ Deletes a question in a given survey

        Args:
            question_id: Id of the question

        Returns:
            If succeeds: True
            If not found: False
        """
        sql = "DELETE FROM \"Questions\" WHERE \"id\"=:question_id"
        result = self.db_connection.session.execute(
            sql, {"question_id": question_id})
        db.session.commit()
        if not result:
            return False
        return True

    def delete_answer_from_question(self, answer_id):
        """ Deletes a answer in a given question

        Args:
            answer_id: Id of the answer

        Returns:
            If succeeds: True
            If not found: False
        """
        sql = "DELETE FROM \"Question_answers\" WHERE \"id\"=:answer_id"
        result = self.db_connection.session.execute(
            sql, {"answer_id": answer_id})
        db.session.commit()
        if not result:
            return False
        return True

    def edit_survey(self, survey_id, name, title, description):
        """ Edits the given survey

        Args:
            survey_id: Id of the survey
            name: Name of the survey
            title: Title of the survey
            description: Description of the survey
        """
        sql = """
        UPDATE "Surveys"
        SET 
            name=:name,
            "updatedAt"=NOW(),
            title_text=:title,
            survey_text=:description
        WHERE id=:survey_id
        RETURNING id
        """
        values = {
            "survey_id": survey_id,
            "name": name,
            "title": title,
            "description": description
        }
        try:
            updated = self.db_connection.session.execute(
                sql, values).fetchone()
            self.db_connection.session.commit()
        except exc.SQLAlchemyError:
            return False
        if updated is not None:
            return updated[0]
        return None

    def get_question(self, question_id):
        """ Gets the text, survey id, category weights,
        and creation time of a question """
        sql = """ SELECT text, "surveyId", "createdAt", category_weights
        FROM "Questions" WHERE id=:question_id """
        question = self.db_connection.session.execute(
            sql, {"question_id": question_id}).fetchone()
        return question

    def create_category(self, name: str, description: str, content_links: list):
        """ Inserts a new category to table Categories based
        and returns Id.

        Returns:
            Id of the new category. """
        sql = """
        INSERT INTO "Categories"
        ("name", "description", "content_links", "createdAt","updatedAt")
        VALUES (:name, :description, :content_links, NOW(), NOW())
        RETURNING id """
        values = {
            "name": name,
            "description": description,
            "content_links": content_links
        }
        try:
            category_id = self.db_connection.session.execute(
                sql, values).fetchone()
            self.db_connection.session.commit()
        except exc.SQLAlchemyError:
            return None
        return category_id[0]
    
    def get_question_answers(self,question_id):
        """ Gets the id:s, texts and points from the answers of
        the question determined by the question_id given """
        sql = """ SELECT id, text, points FROM "Question_answers"
        WHERE "questionId"=:question_id """
        answers = self.db_connection.session.execute(
            sql, {"question_id": question_id}).fetchall()
        return answers
    
    def add_admin(self, email: str):
        """ Inserts a new admin to the Admin table
        
        Returns:
            Id of the new admin """
        
        sql = """
        INSERT INTO "Admins" 
            ("email")
        VALUES 
            (:email) 
        RETURNING id
        """
        values = {"email": email}
        try:
            admin_id = self.db_connection.session.execute(
                sql, values).fetchone()
            self.db_connection.session.commit()
        except exc.SQLAlchemyError:
            return None
        return admin_id[0]
