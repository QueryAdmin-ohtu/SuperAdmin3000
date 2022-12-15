from sqlalchemy import exc
from helper import json_into_dictionary, category_weights_as_json
from db import db


class SurveyRepository:
    """
    A class for interacting with the survey database
    """

    def __init__(self, db_connection=db):
        self.db_connection = db_connection

    def authorized_google_login(self, email):
        """
        Checks whether a Google account is authorized to access the app.

        Returns:
            True if the account is authorized
            False otherwise
        """
        sql = """SELECT id FROM "Admins" WHERE email=:email"""
        result = self.db_connection.session.execute(sql, {"email": email})

        user = result.fetchone()

        if user:
            return True

        return False

    def create_survey(self, name, title, survey_text):
        """ Inserts a survey to table Surveys based
        on given parameters.

        Args:
            name: The name of the survey to be created
            title: The title of the survey
            survey_text: Descriptive text of the survey

        Returns:
            The id of the survey created
        """

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
            Id of the new question.
        """
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
            Id of the new answer
        """
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
        """
        Updates the question to match the new parameters if they differ
        from the current ones.

        Args:
            question_id: The id of the question to be updated
            text: The text of the question
            category_weights: The category weights of the question in JSON
            original_answers: The original answers of the question in a list
            new answers: An updated list of answers to the questions

        Returns:
            True if changes are made
            False if all the parameters matched the old ones
        """

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
        """
        Called from update_question to check if the answers of the
        question have been edited and updates them if they have.

        Args:
            original_answers: A list of the original answers from the question
            new_answers: A list of new potentially edited answers

        Returns:
            True if the lists differ
            False otherwise
        """
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
        """ Deletes a survey from Surveys after deleting all questions, answers,
        categories, results and groups which relate to it. After deletion, checks that
        the survey has been deleted

        Returns:
            True if the survey was deleted
            False otherwise
        """

        questions = self.get_questions_of_survey(survey_id)
        for question in questions:
            answers = self.get_question_answers(question[0])
            for answer in answers:
                sql = """ DELETE FROM "User_answers" WHERE "QuestionAnswerId"=:id """
                db.session.execute(sql, {"id": answer[0]})
                sql = """ DELETE FROM "User_answers" WHERE "questionAnswerId"=:id """
                db.session.execute(sql, {"id": answer[0]})
            sql = """ DELETE FROM "Question_answers" WHERE "questionId"=:id """
            db.session.execute(sql, {"id": question[0]})

        categories = self.get_categories_of_survey(survey_id)
        for category in categories:
            sql = """ DELETE FROM "Category_results" WHERE "categoryId"=:id """
            db.session.execute(sql, {"id": category[0]})

        sql = """ DELETE FROM "Categories" WHERE "surveyId"=:id """
        db.session.execute(sql, {"id": survey_id})
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
        """ Fetches survey data by id

        Returns: survey object (fields: id, name, createdAt, updatedAt, title_text, survey_text)
        """

        sql = """ SELECT * FROM "Surveys" WHERE id=:id """
        survey = self.db_connection.session.execute(
            sql, {"id": survey_id}).fetchone()
        if not survey:
            return False
        return survey

    def get_all_surveys(self):
        """ Fetches all surveys, counts the questions and submissions for each survey

        Returns: List where each item contains the survey

        [0] id
        [1] title
        [2] question count
        [3] submission count
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

        # convert a list of sqlalchemy row objects to a list of lists
        surveys[:] = map(list, surveys)

        return surveys

    def get_questions_of_survey(self, survey_id):
        """ Fetches questions of a given survey
        Args:
          survey_id: Id of the survey

        Returns:
          An array containing each question object;
          question object fields: id, text, surveyId, category_weights, createdAt, updatedAt
        """
        sql = """SELECT * FROM "Questions" WHERE "Questions"."surveyId"=:survey_id ORDER BY id"""
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
        sql = """SELECT id, name FROM "Surveys" WHERE lower(name)=:survey_name"""
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
        """ Looks up all the information of a category based on its id.

        Returns:
            False if the category is not found
            Otherwise, the following list:
            id, name, description, content_links, createdAt, updatedAt, surveyId
        """
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
        sql = """Select "surveyId" from "Questions"  WHERE id=:question_id"""
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
        answers = self.get_question_answers(question_id)
        for answer in answers:
            sql = """ DELETE FROM "User_answers" WHERE "QuestionAnswerId"=:answer_id """
            self.db_connection.session.execute(sql, {"answer_id": answer[0]})
            sql = """ DELETE FROM "User_answers" WHERE "questionAnswerId"=:answer_id """
            self.db_connection.session.execute(sql, {"answer_id": answer[0]})

        sql = """ DELETE FROM "Question_answers" WHERE "questionId"=:question_id """
        self.db_connection.session.execute(sql, {"question_id": question_id})

        sql = """DELETE FROM "Questions" WHERE id=:question_id"""
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
        sql = """SELECT "questionId" FROM "Question_answers"  WHERE id=:answer_id"""
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
        sql = """DELETE FROM "Question_answers" WHERE id=:answer_id"""
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

        Returns:
            True if the survey gets edited
            False otherwise
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
        """ Returns the text, survey id, category weights,
        creation and update time of a question
        """
        sql = """ SELECT text, "surveyId", "createdAt", category_weights, "updatedAt"
        FROM "Questions" WHERE id=:question_id """
        question = self.db_connection.session.execute(
            sql, {"question_id": question_id}).fetchone()
        return question

    def create_category(self, survey_id: str, name: str, description: str, content_links: list):
        """
        Inserts a new category to database table Categories based on parameters given.

        Returns:
            Id of the new category if succesfull.
            None if not succesfull
        """

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
        the question determined by the question_id given
        """

        sql = """ SELECT id, text, points FROM "Question_answers"
        WHERE "questionId"=:question_id """
        answers = self.db_connection.session.execute(
            sql, {"question_id": question_id}).fetchall()
        return answers

    def get_user_answers(self, answer_id):
        """ Gets the id, user id and both question_answer_id AND Question_answer_id of
        the answer determined by the given answer_id
        """

        sql = """ SELECT * FROM "User_answers"
        WHERE answer_id=:answer_id """
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
            Id of the new admin
            None if the admin already exists
        """

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
            False if no
        """

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
                and email of the authorized user
            None if no admins exist
        """
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
        """
        Updates category in the database based on given parameters.

        Returns:
            False if the updating fails
            Otherwise, the category_id of the category updated
        """
        category = self.get_category(category_id)
        if category:
            if category[1] != name:
                self.update_category_in_questions(
                    category[6], category[1], name)

        sql = """ UPDATE "Categories" SET name=:name, description=:description,
        content_links=:content_links, "updatedAt"=:updated 
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
            self.update_survey_updated_at(category[6])
            return updated[0]
        return None

    def update_category_in_questions(self, survey_id, original_name, new_name):
        """ Takes a survey id and goes through every question related to
        it. In the category weights of those questions, it renames the
        category with the original name to the new name. The function is
        only called from update_category and doesn't return anything. """
        questions = self.get_questions_of_survey(survey_id)
        categories = self.get_categories_of_survey(survey_id)
        for question in questions:
            weights = json_into_dictionary(question[3])
            try:
                weights[original_name]
            except KeyError:
                continue
            new_categories = []
            multipliers = {}
            for category in categories:
                if category[1] == original_name:
                    new_categories.append(
                        [category[0], new_name, category[2], category[3]])
                else:
                    new_categories.append(category)
                try:
                    multipliers["cat"+str(category[0])] = weights[category[1]]
                except KeyError:
                    multipliers["cat"+str(category[0])] = 0.0
            category_weights = category_weights_as_json(
                new_categories, multipliers)
            sql = """ UPDATE "Questions" SET category_weights=:category_weights,
            "updatedAt"=:updated WHERE id=:question_id """
            values = {"category_weights": category_weights, "updated": "NOW()",
                      "question_id": question[0]}
            self.db_connection.session.execute(sql, values)
        self.db_connection.session.commit()

    # TODO the name of the function doesn't reflect what it actually does?
    def remove_category_from_question(self, question_id, weights):
        """
        Updates the category weights in the given question

        Returns:
            None if the updating fails
            Otherwise the new weights of the question
        """

        sql = """
        UPDATE "Questions"
        SET category_weights=:category_weights, "updatedAt"=NOW()
        WHERE id=:question_id 
        RETURNING category_weights"""
        values = {
            "category_weights": weights,
            "question_id": question_id
        }
        try:
            new_weights = self.db_connection.session.execute(
                sql, values).fetchone()
            self.db_connection.session.commit()
        except exc.SQLAlchemyError:
            return None
        return new_weights[0]

    def delete_category(self, category_id: str):
        """ Deletes a category from the database
        based on the category_id. Returns True if successful.
        """

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

    def get_category_id_from_name(self, survey_id, category_name):
        """
        Returns the category Id based on the category name if successful.
        Else returns None.
        """
        sql = """
            SELECT c.id FROM "Categories" AS c, "Surveys" as s WHERE c.name = :category_name AND c."surveyId" = :survey_id AND s.id = :survey_id
        """
        values = {"category_name": category_name, "survey_id": survey_id}
        found_id = self.db_connection.session.execute(sql, values).fetchone()
        if found_id:
            return found_id[0]
        return None

    def get_survey_results(self, survey_id):
        """Get the results of a survey

        Return table with columns: id, text, cutoff_from_maxpoints
        """
        sql = """
            SELECT id, text, cutoff_from_maxpoints
            FROM "Survey_results"
            WHERE "surveyId"=:survey_id
            ORDER BY cutoff_from_maxpoints
            """
        result = self.db_connection.session.execute(
            sql, {"survey_id": survey_id}).fetchall()
        return result

    def create_survey_result(self, survey_id, text, cutoff_from_maxpoints):
        """
        Create a new survey result based on parameters given. Results connected
        to the same survey with duplicate cutoff values will not be created

        Returns
            The id of the survey result created
            None if the creation fails
        """
        sql = """
            INSERT INTO "Survey_results"
            ("surveyId", text, cutoff_from_maxpoints, "createdAt", "updatedAt")
            SELECT * FROM (SELECT :survey_id, :text, :cutoff, NOW(), NOW()) AS tmp
            WHERE NOT EXISTS (SELECT cutoff_from_maxpoints FROM "Survey_results"
                WHERE cutoff_from_maxpoints=:cutoff AND "surveyId"=:survey_id)
            RETURNING id
        """
        values = {"survey_id": int(
            survey_id), "text": text, "cutoff": float(cutoff_from_maxpoints)}
        survey_result = self.db_connection.session.execute(
            sql, values).fetchone()
        db.session.commit()
        if survey_result:
            self.update_survey_updated_at(survey_id)
            survey_result_id = survey_result[0]
            return survey_result_id
        return None

    def delete_survey_result(self, result_id):
        """ Delete the given result

            Returns True if success, False if error
        """
        sql = """ DELETE FROM "Survey_results" WHERE id=:result_id """
        values = {"result_id": int(result_id)}

        try:
            self.db_connection.session.execute(sql, values)
            self.db_connection.session.commit()
        except exc.SQLAlchemyError:
            return False
        return True

    def create_category_result(self, category_id: int, text: str, cutoff: float):
        """
        Creates a category result based on given parameters

        Returns:
            Id of the created category results
            None if creation fails
        """

        sql = """
            INSERT INTO "Category_results"
            ("categoryId", text, cutoff_from_maxpoints, "createdAt", "updatedAt")
            SELECT :category_id, :text, :cutoff, NOW(), NOW()
            WHERE NOT EXISTS (SELECT cutoff_from_maxpoints FROM "Category_results"
                WHERE cutoff_from_maxpoints=:cutoff AND "categoryId"=:category_id)
            RETURNING id
            """

        values = {
            "category_id": category_id,
            "text": text,
            "cutoff": cutoff
        }

        try:
            category_result_id = self.db_connection.session.execute(
                sql, values).fetchone()
            self.db_connection.session.commit()
        except exc.SQLAlchemyError:
            return None
        if category_result_id:
            return category_result_id[0]
        return None

    def update_category_and_survey_updated_at(self, category_id, survey_id):
        """
        Updates the updated_at fields of a given category and survey.
        Does not return anything.
        """
        sql1 = """
        UPDATE "Categories"
        SET
            "updatedAt"=NOW()
        WHERE id=:category_id
        """
        values1 = {
            "category_id": category_id}

        sql2 = """
        UPDATE "Surveys"
        SET
            "updatedAt"=NOW()
        WHERE id=:survey_id
        """
        values2 = {
            "survey_id": survey_id}

        db.session.execute(sql1, values1)
        db.session.execute(sql2, values2)
        db.session.commit()

    def get_category_results_from_category_id(self, category_id):
        """
        Selects id, text and cutoff from all category_results linked to a given category_id
        Returns: A list of category_result objects
        """
        sql = """
        SELECT id, text, cutoff_from_maxpoints
            FROM "Category_results"
            WHERE "categoryId"=:category_id
            ORDER BY cutoff_from_maxpoints
        """
        category_results = self.db_connection.session.execute(
            sql, {"category_id": category_id}).fetchall()

        if not category_results:
            return None
        return category_results

    def update_survey_results(self, original_results, new_results, survey_id):
        """ Goes through the lists of results and updates each
        result where the original and new result don't match.

        Returns:
            True if successful
        """

        for i in range(len(original_results)):
            if original_results[i] != new_results[i]:
                sql = """
                UPDATE "Survey_results"
                SET
                    text=:text,
                    cutoff_from_maxpoints=:cutoff,
                    "updatedAt"=NOW()
                WHERE id=:result_id
                """
                values = {
                    "text": new_results[i][1],
                    "cutoff": new_results[i][2],
                    "result_id": new_results[i][0]}
                db.session.execute(sql, values)
        db.session.commit()
        return self.update_survey_updated_at(survey_id)

    def update_category_results(self, original_results, new_results, survey_id):
        """ Goes through the lists of results and updates each
        result where the original and new result don't match.
        This function is not called if there are no differences
        so the updatedAt of the survey in question will also be
        updated and True is returned.
        """
        for i in range(len(original_results)):
            if original_results[i] != new_results[i]:
                sql = """
                UPDATE "Category_results"
                SET
                    text=:text,
                    cutoff_from_maxpoints=:cutoff,
                    "updatedAt"=NOW()
                WHERE id=:result_id
                """
                values = {
                    "text": new_results[i][1],
                    "cutoff": new_results[i][2],
                    "result_id": new_results[i][0]}
                db.session.execute(sql, values)
        db.session.commit()
        return self.update_survey_updated_at(survey_id)

    def delete_category_result(self, category_result_id):
        """ Delete the given category result

            Returns True if success, False if error
        """
        sql = """ DELETE FROM "Category_results" WHERE id=:category_result_id """

        try:
            values = {"category_result_id": int(category_result_id)}
            self.db_connection.session.execute(sql, values)
            self.db_connection.session.commit()
        except ValueError or exc.SQLAlchemyError:
            return False
        return True

    def delete_category_results_of_category(self, category_id):
        """
        Deletes all category results for the given category.
        Returns True if successful and otherwise False. """
        sql = """
        DELETE FROM "Category_results"
        WHERE "categoryId"=:category_id
        """

        try:
            values = {
                "category_id": category_id
            }
            self.db_connection.session.execute(sql, values)
            self.db_connection.session.commit()
        except exc.SQLAlchemyError:
            return False
        return True

    def get_category_results_from_category_result_id(self, category_result_id):
        """
        Selects all category_results linked to a given category_result_id

        Returns: A list of category_result objects in this order:
        id, categoryId, text, cutoff_from_maxpoints, createdAt, updatedAt
        """
        sql = """
        SELECT * FROM "Category_results"
        WHERE id = :category_result_id
        """
        category_results = self.db_connection.session.execute(
            sql, {"category_result_id": category_result_id}).fetchall()

        if not category_results:
            return None
        return category_results

    def survey_status_handle_questions(self, questions, questions_without_answers,
                                       questions_without_categories, categories_with_questions):
        """
        Goes through the list of questions given and adds the texts
        from them to the other lists given if they fill the proper
        criteria specified by the names of the lists.
        """
        for question in questions:
            if self.get_question_answers(question[0]) == []:
                questions_without_answers.append(question[1])
            question_category_weights = json_into_dictionary(question[3])
            if self.all_category_weights_equal_0(question_category_weights):
                questions_without_categories.append(question[1])
            for key in question_category_weights:
                if question_category_weights[key] != float(0.0):
                    categories_with_questions.append(question[1])

    def all_category_weights_equal_0(self, category_weights_as_dict):
        """
        Check if all category_weight values are equal to 0.0.
        Returns True if they are and False otherwise.
        """
        return list(set(list(category_weights_as_dict.values()))) == [0.0]

    def get_unrelated_categories_in_weights(self, categories, questions):
        """ Go through all questions in a survey and check the category
        names in the weights of the question. If the category name
        can not be found in the categories of the survey, the name
        is added to the dictionary to be returned.

        Args:
            categories:  All the categories of the survey
            questions:   All the questions of the survey

        Returns:
            A dictionary, where the key is the question id,
            and values are a list of category names:
            {1: ["foo", "bar"], 5: ["baz"]}
        """
        result = {}
        category_names = []

        for category in categories:
            category_names.append(category[1])

        for question in questions:
            name_list = []

            weights_json = question[3]
            weights = json_into_dictionary(weights_json)

            for weight_name in weights.keys():
                if weight_name not in category_names:
                    name_list.append(weight_name)

            if name_list != []:
                result[question[1]] = name_list

        return result

    def check_survey_status(self, survey_id):
        """
        Checks the status of a survey. Returns a list with information and a status where:
        - 'red' = critical error:
            - no survey results exist
            - no category results exist
            - survey contains no questions
            - there are questions without answers
            - survey contains no categories
            - category weights in questions not found in categories
        - 'yellow' = missing information:
            - there are questions without categories
            - there are categories without questions
        - 'green' = Survey is complete.

        Returns a list as follows:

        [0]    status  : (str) 'red','yellow' or 'green',
        [1]    no_survey_results : (bool),
        [2]    no_categories : (bool),
        [3]    unrelated_categories_in_weights : (list) [category names]
        [4]    no_questions : (bool),
        [5]    questions_without_answers :(list) [question names],
        [6]    questions_without_categories :(list) [category names],
        [7]    categories_without_questions : (list) [category names]
        [8]    categories_without_results :
                (dictionary) {question_id: [category names]},


        """
        categories = self.get_categories_of_survey(survey_id)
        questions = self.get_questions_of_survey(survey_id)

        no_survey_results = self.get_survey_results(survey_id) == []
        no_categories = self.get_categories_of_survey(survey_id) == []
        no_questions = self.get_questions_of_survey(survey_id) == []

        unrelated_categories_in_weights = \
            self.get_unrelated_categories_in_weights(categories, questions)

        categories_without_results = []
        questions_without_answers = []
        questions_without_categories = []
        categories_with_questions = []
        categories_without_questions = []

        self.survey_status_handle_questions(questions,
                                            questions_without_answers,
                                            questions_without_categories,
                                            categories_with_questions)

        for category in categories:
            if self.get_category_results_from_category_id(category[0]) is None:

                categories_without_results.append(category[1])

                if category[1] not in categories_with_questions:
                    categories_without_questions.append(category[1])

        if no_survey_results or \
           categories_without_results or \
           questions_without_answers or \
           no_categories or \
           no_questions:
            status = "red"

        elif questions_without_categories or \
                categories_without_questions or \
                unrelated_categories_in_weights:
            status = "yellow"

        else:
            status = "green"

        return [
            status,
            no_survey_results,
            no_categories,
            categories_without_results,
            no_questions,
            questions_without_answers,
            questions_without_categories,
            categories_without_questions,
            unrelated_categories_in_weights
        ]
