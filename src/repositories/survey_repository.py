import uuid
from datetime import datetime
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

    def update_question(self, question_id, text, category_weights, original_answers, new_answers):
        """ Checks if the parameters of the question determined by the question_id
        match the parameters given to the function. These parameters include the
        text and category weights of the question and the contents of the answers
        belonging to the question. If these parameters match, nothing is changed
        and False is returned, otherwise the parameters will be updated to match
        the ones given to the function and True will be returned. """
        original = self.get_question(question_id)
        sql2 = False
        sql3 = False
        answers_updated = False
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

        if original_answers:
            answers_updated = self.update_answers(
                original_answers, new_answers)

        if sql2 or sql3 or answers_updated:
            self.db_connection.session.commit()
            self.update_question_updated_at(question_id)
            self.update_survey_updated_at(survey_id)

        return sql2 or sql3 or answers_updated

    def update_answers(self, original_answers, new_answers):
        """ Goes through the given list of answer ids and
        checks if the current information matches with the
        information from the lists given. If everything
        matches False is returned and otherwise True """
        updated = False
        for i in range(len(new_answers)):
            if original_answers[i] != new_answers[i]:
                updated = True
                sql = """
                UPDATE "Question_answers"
                SET 
                    text=:text,
                    points=:points,
                    "updatedAt"=NOW()
                WHERE id=:answer_id
                """
                values = {
                    "text": new_answers[i][1],
                    "points": new_answers[i][2],
                    "answer_id": new_answers[i][0]}
                db.session.execute(sql, values)
        if updated:
            db.session.commit()
        return updated

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
        """ Fetches all surveys, counts the questions and
        submissions for each survey

        Returns: List where each item contains the survey
        id, title, question count and submission count
        """
        sql = """
        SELECT
            s.id,
            s.title_text,
            COUNT(DISTINCT q.id) AS questions,
            COUNT(DISTINCT ua."createdAt") AS submissions
        FROM "Surveys" AS s
        LEFT JOIN "Questions" AS q
            ON s.id = q."surveyId"
        LEFT JOIN "Question_answers" AS qa
            ON q.id = qa."questionId"
        LEFT JOIN "User_answers" AS ua
            ON qa.id = ua."questionAnswerId"
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
            True, id if matching name found, False, None if not
        """
        sql = "SELECT id, name FROM \"Surveys\" WHERE lower(name)=:survey_name"
        result = self.db_connection.session.execute(
            sql, {"survey_name": survey_name.lower()})

        survey = result.fetchone()

        if survey:
            return True, survey.id
        return False, None

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

    def get_users_who_answered_survey(self,
                                      survey_id: int,
                                      start_date: datetime = None,
                                      end_date: datetime = None,
                                      group_name=None,
                                      email=""):
        """ Returns a list of users who have answered a given survey.
        Results can be filtered by a timerange, group name and email address.
        Args:
            survey_id: Id of the survey
            start_time: Start of timerange to filter by (optional)
            end_time: End of timerange to filter by (optional)
            group_name: User group to filter by (optional)
            email: Email to filter by (optional)

        Returns:
            On succeed: A list of lists where each element contains
                [id, email, group_name, answer_time]
            On error / no users who answered found:
                None
        """
        print(f"Email: '{email}'", flush=True)

        sql = """
        SELECT
            DISTINCT "u"."id",
            "u"."email",
            "sua"."group_name",
            "ua"."updatedAt" as answer_time
        FROM
            "Users" as u
        LEFT JOIN "User_answers" as ua
            ON "u"."id" = "ua"."userId"
        LEFT JOIN "Question_answers" as qa
            ON "ua"."questionAnswerId" = "qa"."id"
        LEFT JOIN "Questions" as q
            ON "q"."id" = "qa"."questionId"
        LEFT JOIN "Surveys" as s
            ON "s"."id" = "q"."surveyId"
        LEFT JOIN "Survey_user_groups" as sua
            ON "u"."groupId" = "sua"."id"
        WHERE "s"."id"=:survey_id AND "sua"."surveyId"=:survey_id
            AND ((:start_date IS NULL AND :end_date IS NULL) OR ("ua"."updatedAt" > :start_date AND "ua"."updatedAt" < :end_date))
            AND ((:group_name IS NULL) OR ("group_name"=:group_name))
            AND (("email" LIKE :email))
        """
        values = {"survey_id": survey_id,
                  "start_date": start_date,
                  "end_date": end_date,
                  "group_name": group_name,
                  "email": f"%{email}%"}

        try:
            users = self.db_connection.session.execute(sql, values).fetchall()

            if not users:
                return None
            return users

        except exc.SQLAlchemyError:
            return None

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

    def get_number_of_submissions(self, survey_id, user_group_id=None):
        """ Finds and returns the number of distinct users who have
        submitted answers to a survey."""

        sql = """
        SELECT
            s.id,
            COUNT(DISTINCT ua."createdAt") AS submissions
        FROM "Surveys" AS s
        LEFT JOIN "Questions" AS q
            ON s.id = q."surveyId"
        LEFT JOIN "Question_answers" AS qa
            ON q.id = qa."questionId"
        LEFT JOIN "User_answers" AS ua
            ON qa.id = ua."questionAnswerId"
        LEFT JOIN "Users" AS u
            ON u.id = ua."userId"
        WHERE 
            s.id=:survey_id
            AND (u."groupId"=:group_id OR :group_id IS NULL)
        GROUP BY s.id
        """
        submissions = self.db_connection.session.execute(
            sql, {"survey_id": survey_id, "group_id": user_group_id}).fetchone()

        if not submissions:
            return None
        return submissions.submissions

    def get_answer_distribution(self,
                                survey_id,
                                start_date: datetime = None,
                                end_date: datetime = None,
                                user_group_id: uuid = None,
                                email: str = ""):
        """ Finds and returns the distribution of user answers
        over the answer options of a survey.

        Filtering by date range and/or user group and/or email. Start and end
        dates are included in the query.

        Returns a table where each row contains:
        question id, question text, answer id, answer text, user answer counts
        """

        if end_date:
            end_date = end_date.replace(hour=23, minute=59, second=59)

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
        LEFT JOIN "Users" AS u
            ON u.id = ua."userId"
        WHERE s.id=:survey_id
            AND ((:start_date IS NULL AND :end_date IS NULL) OR (ua."createdAt" BETWEEN :start_date AND :end_date))
            AND ((:group_id IS NULL) OR (u."groupId"=:group_id))
            AND (u."email" LIKE :email)
        GROUP BY q.id, q.text, qa.id, qa.text
        ORDER BY q.id
        """

        values = {"survey_id": survey_id,
                  "group_id": user_group_id,
                  "start_date": start_date,
                  "end_date": end_date,
                  "email": f"%{email}%"}
        try:
            result = self.db_connection.session.execute(sql, values).fetchall()
            if result:
                return result
            return None
        except exc.SQLAlchemyError as exception:
            return exception

    def get_answer_distribution_filtered(self, survey_id,
                                         start_date: datetime = None,
                                         end_date: datetime = None,
                                         group_name: str = "",
                                         email: str = ""):
        """ Finds and returns the distribution of user answers
        over the answer options of a survey.

        Filtering by date range and/or user group and/or email. Start and end
        dates are included in the query.

        Returns a table where each row contains:
        question id, question text, answer id, answer text, user answer counts
        """

        group_id = self._find_user_group_by_name(group_name)

        return self.get_answer_distribution(survey_id, start_date, end_date, group_id, email)

    def _find_user_group_by_name(self, group_name):
        sql = """SELECT id, group_name FROM "Survey_user_groups" WHERE lower(group_name)=:group_name"""
        result = self.db_connection.session.execute(
            sql, {"group_name": group_name.lower()})

        row = result.fetchone()
        group_id = row[0] if row else None

        return group_id

    def _add_user(self, email=None, group_id=None):
        """Adds a user to database for testing purposes

        Returns user id"""

        sql = """INSERT INTO "Users" ("email", "groupId", "createdAt", "updatedAt")
            VALUES (:email, :group_id, NOW(), NOW()) RETURNING id"""
        values = {"email": email, "group_id": group_id}
        user_id = self.db_connection.session.execute(sql, values).fetchone()[0]
        db.session.commit()
        return user_id

    def _add_user_group(self, survey_id):
        """Adds a user group to database for testing purposes.

        Returns database id"""
        group_id = uuid.uuid4()
        sql = """INSERT INTO "Survey_user_groups" (id, "surveyId", "createdAt", "updatedAt")
            VALUES (:group_id, :survey_id, NOW(), NOW()) RETURNING id"""
        group_id = self.db_connection.session.execute(
            sql, {"group_id": group_id, "survey_id": survey_id}).fetchone()[0]
        db.session.commit()
        return group_id

    def _add_user_answers(self, user_id, question_answer_ids: list, answer_time: datetime = None):
        """Adds user answers to database for testing purposes"""

        for id in question_answer_ids:
            sql = """INSERT INTO "User_answers"
                ("userId", "questionAnswerId", "createdAt", "updatedAt")
                VALUES (:user_id, :question_answer_id, :answer_time, :answer_time)"""
            values = {
                "user_id": user_id,
                "question_answer_id": id,
                "answer_time": "NOW()" if answer_time is None else answer_time
            }

            self.db_connection.session.execute(sql, values)
        db.session.commit()

    def _add_survey_user_group(self, group_name, survey_id):
        """
            Adds a survey user group for testing purposes
            Returns:
                Survey_user_groups id (UUID)
        """

        sql = """
        INSERT INTO "Survey_user_groups"
            ("id", "group_name", "surveyId", "createdAt", "updatedAt")
        VALUES (gen_random_uuid(), :group_name, :survey_id, NOW(), NOW())
        RETURNING id
        """
        values = {"group_name": group_name, "survey_id": survey_id}
        survey_user_group_id = self.db_connection.session.execute(
            sql, values).fetchone()[0]
        db.session.commit()
        return survey_user_group_id

    def get_count_of_user_answers_to_a_question(self, question_id):
        """
            Retrieve number of submissions to a given question.

            Returns:
                Amount of user answers if successful. Else returns 0.
        """
        sql = """
        SELECT COUNT(id)
        FROM "User_answers"
        WHERE "questionAnswerId" IN (
            SELECT qa.id
            FROM "Question_answers" as qa, "User_answers" AS ua
            WHERE qa."questionId" = :question_id)
        """
        values = {"question_id": question_id}
        count_of_answers = self.db_connection.session.execute(sql, values).fetchone()[0]
        if count_of_answers:
            return count_of_answers
        return 0

    def get_sum_of_user_answer_points_by_question_id(self, question_id):
        """
            Returns the sum of all user answers for a given question.
        """

        sql =  """
        SELECT
            (COUNT(ua.id) * points)
        FROM "Questions" AS q
        LEFT JOIN "Question_answers" AS qa
            ON q.id = qa."questionId"
        LEFT JOIN "User_answers" AS ua
            ON qa.id = ua."questionAnswerId"
        WHERE q.id=:question_id
        GROUP BY q.id, qa.id
        ORDER BY q.id
        """
        values = {"question_id": question_id}
        sum_of_points = self.db_connection.session.execute(sql, values).fetchall()
        db.session.commit()
        res = 0
        for i in range(0, len(sum_of_points)):
            if sum_of_points[i][0] is not None:
                res += (sum_of_points[i][0])

        return res

    def calculate_average_scores_by_category(self, survey_id):
        """
        Calculates weighted average points for all user answers in a survey.
        Returns a list of tuples which includes the category id, category name and average score
        (to the precision of two decimal places) of all user answers in a given survey.
        """

        result_list = []
        related_questions = self.get_questions_of_survey(survey_id)
        for question in related_questions:
            points = self.get_sum_of_user_answer_points_by_question_id(question.id)
            answers = self.get_count_of_user_answers_to_a_question(question.id)
            if answers == 0:
                continue
            avg = float(points / answers)

            for category_weight in question.category_weights:
                weighted_average = float("{:.2f}".format(avg * category_weight['multiplier']))
                complete_item = (self.get_category_id_from_name(
                    survey_id, category_weight['category']), category_weight['category'], weighted_average)
                result_list.append(complete_item)

        return result_list

    def get_category_id_from_name(self, survey_id, category_name):
        """
        Returns the category Id based on the category name.
        """
        sql = """
            SELECT c.id FROM "Categories" AS c, "Surveys" as s WHERE c.name = :category_name and s.id = :survey_id
        """
        values = {"category_name": category_name, "survey_id": survey_id}
        return self.db_connection.session.execute(sql, values).fetchone()[0]

    def get_survey_results(self, survey_id):
        """Get the results of a survey

        Return table with columns: id, text, cutoff_from_maxpoints, createdAt, updatedAt"""
        sql = """
            SELECT id, text, cutoff_from_maxpoints, "createdAt", "updatedAt"
            FROM "Survey_results"
            WHERE "surveyId"=:survey_id
            """
        result = self.db_connection.session.execute(sql, {"survey_id": survey_id}).fetchall()
        return result

    def create_survey_result(self, survey_id, text, cutoff_from_maxpoints):
        """Create a new survey result.

        Results connected to the same survey with duplicate cutoff values will not be created"""
        sql = """
            INSERT INTO "Survey_results"
            ("surveyId", text, cutoff_from_maxpoints, "createdAt", "updatedAt")
            SELECT * FROM (SELECT :survey_id, :text, :cutoff, NOW(), NOW()) AS tmp
            WHERE NOT EXISTS (SELECT cutoff_from_maxpoints FROM "Survey_results"
                WHERE cutoff_from_maxpoints=:cutoff AND "surveyId"=:survey_id)
            RETURNING id
        """
        values = {"survey_id": int(survey_id), "text": text, "cutoff": float(cutoff_from_maxpoints)}
        survey_result = self.db_connection.session.execute(sql, values).fetchone()
        db.session.commit()
        if survey_result:
            self.update_survey_updated_at(survey_id)
            survey_result_id = survey_result[0]
            return survey_result_id
        return None

    def create_placeholder_category_result(self, category_id):
        """
        Creates a placeholder categy result
        """

        sql = """
            INSERT INTO "Category_results" 
            ("categoryId", "text", cutoff_from_maxpoints, "createdAt", "updatedAt") 
            VALUES (:category_id, 'To be written', 1.0, NOW(), NOW())
            RETURNING id """
        values = {
            "category_id": category_id,
        }

        try:
            category_result_id = self.db_connection.session.execute(
                sql, values).fetchone()
            self.db_connection.session.commit()
        except exc.SQLAlchemyError:
            return None

        return category_result_id[0]

    def get_category_results_from_category_id(self, category_id):
        """
        Selects all category_results linked to a given category_id

        Returns: A list of category_result objects
        """
        sql = """
        SELECT * FROM "Category_results"
        WHERE "categoryId" = :category_id
        """
        category_results = self.db_connection.session.execute(
            sql, {"category_id": category_id}).fetchall()

        if not category_results:
            return None
        return category_results
