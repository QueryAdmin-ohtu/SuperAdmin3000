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

    def create_survey(self, name, title, survey_text):
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
            "survey_text": survey_text
        }

        try:
            survey_id = self.db_connection.session.execute(
                sql, values).fetchone()
            self.db_connection.session.commit()
        except exc.SQLAlchemyError:
            return None

        return survey_id[0]

    def update_survey_updated_at(self, survey_id):
        """ Updates the surveys updatedAt field.
        
        Returns: 
            True if successful
        """
        sql = """ UPDATE "Surveys" SET "updatedAt"=NOW()
        WHERE id=:survey_id """
        self.db_connection.session.execute(
            sql, {"survey_id": survey_id})
        self.db_connection.session.commit()
        return True

    def update_question_updated_at(self, question_id):
        """ Updates the given questions updatedAt field.

        Returns:
            True if successful
        """
        sql = """ UPDATE "Questions" SET "updatedAt"=NOW() WHERE id=:question_id """
        self.db_connection.session.execute(
            sql, {"question_id": question_id})
        self.db_connection.session.commit()
        return True

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
        self.update_survey_updated_at(survey_id)
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
        survey_id = self.get_survey_id_from_question_id(question_id)
        self.update_question_updated_at(question_id)
        self.update_survey_updated_at(survey_id)
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
        survey_id = self.get_survey_id_from_question_id(question_id)  
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
        self.update_question_updated_at(question_id)
        self.update_survey_updated_at(survey_id)
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
        related to each survey

        Returns: List where each item contains the survey
        id, title, question count and submission count are
        included """
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

    def survey_exists(self, survey_name):
        """Checks if a survey with identical name already exists. Case insensitive.

        Args:
            survey_name: Name of the new survey

        Returns:
            True if matching name found, False if not
        """
        sql = "SELECT name FROM \"Surveys\" WHERE lower(name)=:survey_name"
        result = self.db_connection.session.execute(
            sql, {"survey_name": survey_name.lower()})

        survey_found = result.fetchone()

        if survey_found:
            return True
        return False

    def get_all_categories(self):
        """ Fetches all categories from the database.

        Returns:
        An array containing id, name, description, content_links of each category.
        """
        sql = """ SELECT id, name, description, content_links FROM "Categories" """
        result = self.db_connection.session.execute(sql)

        categories = result.fetchall()

        return categories

    def get_category(self, category_id):
        """ Looks up category based on
        id and returns its data in a list.
        Return False if category is not found."""
        sql = """ SELECT * FROM "Categories" WHERE id=:id """
        try:
            category = self.db_connection.session.execute(
                sql, {"id": category_id}).fetchone()
        except exc.SQLAlchemyError:
            return False
        return category

    def get_categories_of_survey(self, survey_id):
        """ Fetches categories of a given survey from the database.

        Returns:
        An array containing id, name, description, content_links of the categories.
        """
        sql = """ SELECT id, name, description, content_links FROM "Categories"
        WHERE "surveyId"=:survey_id ORDER BY id"""

        categories = self.db_connection.session.execute(
            sql, {"survey_id": survey_id}).fetchall()

        return categories

    def get_survey_id_from_question_id(self, question_id):
        """ Returns the id of the parent survey
        Args:
            question_id: Id of the question
        
        Returns:
            If succeeds: survey_id
        """
        sql = "Select \"surveyId\" from \"Questions\"  WHERE \"id\"=:question_id"
        result = self.db_connection.session.execute(
            sql, {"question_id": question_id}).fetchall()
        db.session.commit()
        if result:
            return result[0][0]
        return None

    def delete_question_from_survey(self, question_id):
        """ Deletes a question in a given survey

        Args:
            question_id: Id of the question

        Returns:
            If succeeds: True
            If not found: False
        """
        survey_id = self.get_survey_id_from_question_id(question_id)
        
        sql = "DELETE FROM \"Questions\" WHERE \"id\"=:question_id"
        result = self.db_connection.session.execute(
            sql, {"question_id": question_id})
        db.session.commit()
        if not result:
            return False
        self.update_survey_updated_at(survey_id)
        return True

    def get_question_id_from_answer_id(self, answer_id):
        """ Returns the id of the parent question
        Args:
            answer_id: Id of the answer
        
        Returns:
            If succeeds: question_id
        """
        sql = "Select \"questionId\" from \"Question_answers\"  WHERE \"id\"=:answer_id"
        result = self.db_connection.session.execute(
            sql, {"answer_id": answer_id}).fetchall()
        db.session.commit()
        if result:
            return result[0][0]
        return None

    def delete_answer_from_question(self, answer_id):
        """ Deletes a answer in a given question

        Args:
            answer_id: Id of the answer

        Returns:
            If succeeds: True
            If not found: False
        """
        sql = "DELETE FROM \"Question_answers\" WHERE \"id\"=:answer_id"
        question_id = self.get_question_id_from_answer_id(answer_id)
        survey_id = self.get_survey_id_from_question_id(question_id)
        result = self.db_connection.session.execute(
            sql, {"answer_id": answer_id})
        db.session.commit()
        if not result:
            return False
        self.update_question_updated_at(question_id)
        self.update_survey_updated_at(survey_id)
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
        creation and update time of a question """
        sql = """ SELECT text, "surveyId", "createdAt", category_weights, "updatedAt"
        FROM "Questions" WHERE id=:question_id """
        question = self.db_connection.session.execute(
            sql, {"question_id": question_id}).fetchone()
        return question

    def create_category(self, survey_id: str, name: str, description: str, content_links: list):
        """ Inserts a new category to database table Categories.

        Returns:
            Id of the new category if succesfull.
            None if not succesfull """

        sql = """
        INSERT INTO "Categories"
        ("surveyId", "name", "description", "content_links", "createdAt","updatedAt")
        VALUES (:survey_id, :name, :description, :content_links, NOW(), NOW())
        RETURNING id """
        values = {
            "survey_id": survey_id,
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
        self.update_survey_updated_at(survey_id)
        return category_id[0]

    def get_question_answers(self, question_id):
        """ Gets the id:s, texts and points from the answers of
        the question determined by the question_id given """

        sql = """ SELECT id, text, points FROM "Question_answers"
        WHERE "questionId"=:question_id """
        answers = self.db_connection.session.execute(
            sql, {"question_id": question_id}).fetchall()
        return answers

    def get_user_answers(self, answer_id):
        """ Gets the id, user id and both question_answer_id AND Question_answer_id of
        the answer determined by the given answer_id """

        sql = """ SELECT * FROM \"User_answers\"
        WHERE "answer_id"=:answer_id"""
        try:
            answers = self.db_connection.session.execute(
                sql, {"id": answer_id}).fetchall()
        except exc.SQLAlchemyError:
            return None
        return answers

    def add_admin(self, email: str):
        """ Inserts a new admin to the Admin table if it does not
        exist already

        Returns:
            Id of the new admin """

        if not self._admin_exists(email):
            sql = """
            INSERT INTO "Admins" (email)
            VALUES (:email)
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
        return None

    def _admin_exists(self, email):
        """ Test if the given email is already one of the
        authorized users

        Returns:
            True if yes,
            False if no """

        values = {"email": email}
        sql = """
        SELECT *
        FROM "Admins"
        WHERE email=:email
        """
        try:
            result = self.db_connection.session.execute(
                sql, values).fetchone()
        except exc.SQLAlchemyError:
            return False
        if not result:
            return False
        return True

    def get_all_admins(self):
        """ Fetches all authorized users from the database

        Returns:
            List where each item contains a tuple with the id
            and email of the authorized user """
        sql = """
        SELECT * FROM "Admins"
        ORDER BY id
        """
        admins = self.db_connection.session.execute(
            sql).fetchall()
        if not admins:
            return None
        return admins

    def update_category(self, category_id: str, content_links: list, name: str, description: str):
        """ Updates category in the database.
        If succesful returns category_id."""

        sql = """ UPDATE "Categories" SET "name"=:name, "description"=:description,
        "content_links"=:content_links, "updatedAt"=:updated 
        WHERE id=:category_id RETURNING id"""

        values = {"category_id": category_id, "name": name, "description": description,
                  "content_links": content_links, "updated": "NOW()"}

        try:
            updated = self.db_connection.session.execute(
                sql, values).fetchone()
            self.db_connection.session.commit()
        except exc.SQLAlchemyError:
            return False
        if updated is not None:
            category = self.get_category(category_id)
            self.update_survey_updated_at(category[6])
            return updated[0]
        return None

    def delete_category(self, category_id: str):
        """ Deletes a category from the database
        based on the category_id. Returns True if successful. """

        category = self.get_category(category_id)
        if not category:
            return False
        try:
            sql = """ DELETE FROM "Categories" WHERE id=:category_id """
            self.db_connection.session.execute(
                sql, {"category_id": category_id})
            self.db_connection.session.commit()
        except exc.SQLAlchemyError as exception:
            return exception
        self.update_survey_updated_at(category[6])
        return True

    def get_number_of_submissions(self, survey_id):
        """ Finds and returns the number of distinct users who have
        submitted answers to a survey."""

        # TODO: filter by dates/groups

        sql = """
        SELECT
            s.id,
            COUNT(DISTINCT ua."userId") AS submissions
        FROM "Surveys" AS s
        LEFT JOIN "Questions" AS q
            ON s.id = q."surveyId"
        LEFT JOIN "Question_answers" AS qa
            ON q.id = qa."questionId"
        LEFT JOIN "User_answers" AS ua
            ON qa.id = ua."questionAnswerId"
        WHERE s.id=:survey_id
        GROUP BY s.id
        """
        submissions = self.db_connection.session.execute(
            sql, {"survey_id": survey_id}).fetchone()

        if not submissions:
            return None
        return submissions.submissions

    def get_answer_distribution(self, survey_id):
        """ Finds and returns the distribution of user answers
        over the answer options of a survey.

        Returns a table with question id, question text, answer id, answer text,
        user answer counts"""

        # TODO: filter by dates/groups

        sql = """
        SELECT
            q.id AS question_id,
            q.text AS question,
            qa.id AS answer_id,
            qa.text AS answer,
            COUNT(ua.id)
        FROM "Surveys" AS s
        LEFT JOIN "Questions" AS q
            ON s.id = q."surveyId"
        LEFT JOIN "Question_answers" AS qa
            ON q.id = qa."questionId"
        LEFT JOIN "User_answers" AS ua
            ON qa.id = ua."questionAnswerId"
        WHERE s.id=:survey_id
        GROUP BY q.id, q.text, qa.id, qa.text
        """
        result = self.db_connection.session.execute(
            sql, {"survey_id": survey_id}).fetchall()

        return result

    def _add_user(self):
        """Adds a user to database for testing purposes

        Returns user id"""

        sql="""INSERT INTO "Users" ("createdAt", "updatedAt")
            VALUES (NOW(), NOW()) RETURNING id"""
        user_id = self.db_connection.session.execute(sql).fetchone()[0]
        db.session.commit()
        return user_id

    def _add_user_answer(self, user_id, question_answer_id):
        """Adds a user answer to database for testing purposes"""

        sql="""INSERT INTO "User_answers"
            ("userId", "questionAnswerId", "createdAt", "updatedAt")
            VALUES (:user_id, :question_answer_id, NOW(), NOW())"""
        values = {"user_id": user_id, "question_answer_id": question_answer_id}

        self.db_connection.session.execute(sql, values)
        db.session.commit()
