import uuid
from datetime import datetime
from sqlalchemy import exc
from db import db
from repositories.survey_repository import SurveyRepository


class StatisticRepository:
    """
    A class for interacting with the survey database in
    order to calculate the statistics of surveys
    """

    def __init__(self, db_connection=db):
        self.db_connection = db_connection
        self.repo = SurveyRepository()

    def get_users_who_answered_survey(self,
                                      survey_id: int,
                                      start_date: datetime = None,
                                      end_date: datetime = None,
                                      group_id=None,
                                      email=""):
        """ Returns a list of users who have answered a given survey.
        Results can be filtered by a timerange, group name and email address.
        Args:
            survey_id: Id of the survey
            start_time: Start of timerange to filter by (optional)
            end_time: End of timerange to filter by (optional)
            group_id: User group to filter by (optional)
                        If the group is None, all users all listed. If the
                        group is string "None", only users without any group
                        are listed.
            email: Email to filter by (optional)

        Returns:
            On succeed: A list of lists where each element contains
                [id, email, group_id, group_name, answer_time]
            On error / no users who answered found:
                None
        """
        sql = """
        SELECT
            DISTINCT u.id,
            u.email,
            sua.id as group_id,
            sua.group_name,
            ua."updatedAt" as answer_time
        FROM
            "Users" as u
        LEFT JOIN "User_answers" as ua
            ON u.id = ua."userId"
        LEFT JOIN "Question_answers" as qa
            ON ua."questionAnswerId" = qa.id
        LEFT JOIN "Questions" as q
            ON q.id = qa."questionId"
        LEFT JOIN "Surveys" as s
            ON s.id = q."surveyId"
        LEFT OUTER JOIN "Survey_user_groups" as sua
            ON u."groupId" = sua.id
        WHERE s.id=:survey_id
            AND ((:start_date IS NULL AND :end_date IS NULL) OR (ua."updatedAt" > :start_date AND ua."updatedAt" < :end_date))
            AND ((:group_id IS NULL) OR
                 (sua.id=:group_id))
            AND COALESCE (email, '') like :email
        """
        values = {"survey_id": survey_id,
                  "start_date": start_date,
                  "end_date": end_date,
                  "group_id": group_id,
                  "email": f"%{email}%"}

        try:
            users = self.db_connection.session.execute(sql, values).fetchall()

            if not users:
                return None
            return users

        except exc.SQLAlchemyError:
            return None

    def get_number_of_submissions(self, survey_id, user_group_id=None):
        """
        Finds and returns the number of distinct users who have
        submitted answers to a survey.

        Args:
            survey_id: Id of the survey to calculate submissions of
            user_group_id: None by default but if a value is given, only the submission
                            by users belonging to the group will be counted

        Returns:
            None if there are no submissions and otherwise how many there are
        """

        # TODO:
        # Handle situation, where we want to filter in only users without any groups
        # currently group id None lists all users
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

        Args:
            survey_id: Id of the survey to get the answer distribution of
            start_date: None by default, takes only the answers given after this date into account if specified
            end_date: None by default, takes only the answers given before this date into account if specified.
                If start or end date is given, the other must be also given.
            user_group_id:  None by default but if specified, only accounts the answers given by users in the group
            email: "" by default but when given, makes the function only take the answers into
                account which were given by users with the given phrase in their email

        Returns:
            A table where each row contains:
            question id, question text, answer id, answer text, user answer counts
        """

        if end_date:
            end_date = end_date.replace(hour=23, minute=59, second=59)

        # TODO:
        # Handle situation, where we want to filter in only users without any groups
        # currently group id None lists all users
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
            AND (COALESCE (u."email", '') LIKE :email)
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

    def find_user_group_by_name(self, group_name):
        """Finds and returns user group id by user group name
        """
        sql = """SELECT id, group_name FROM "Survey_user_groups" WHERE lower(group_name)=:group_name"""
        result = self.db_connection.session.execute(
            sql, {"group_name": group_name.lower()})

        row = result.fetchone()
        group_id = row[0] if row else None

        return group_id

    def _add_user(self, email=None, group_id=None):
        """Helper method: Adds a user to database for testing purposes

        Returns user id
        """

        sql = """INSERT INTO "Users" ("email", "groupId", "createdAt", "updatedAt")
            VALUES (:email, :group_id, NOW(), NOW()) RETURNING id"""
        values = {"email": email, "group_id": group_id}
        user_id = self.db_connection.session.execute(sql, values).fetchone()[0]
        db.session.commit()
        return user_id

    def _add_user_group(self, survey_id):
        """Helper method: Adds a user group to database for testing purposes.

        Returns database id
        """
        group_id = uuid.uuid4()
        sql = """INSERT INTO "Survey_user_groups" (id, "surveyId", "createdAt", "updatedAt")
            VALUES (:group_id, :survey_id, NOW(), NOW()) RETURNING id"""
        group_id = self.db_connection.session.execute(
            sql, {"group_id": group_id, "survey_id": survey_id}).fetchone()[0]
        db.session.commit()
        return group_id

    def _add_user_answers(self, user_id, question_answer_ids: list, answer_time: datetime = None):
        """Helper method: Adds user answers to database for testing purposes.

        Does not return anything
        """

        for qa_id in question_answer_ids:
            sql = """INSERT INTO "User_answers"
                ("userId", "questionAnswerId", "createdAt", "updatedAt")
                VALUES (:user_id, :question_answer_id, :answer_time, :answer_time)"""
            values = {
                "user_id": user_id,
                "question_answer_id": qa_id,
                "answer_time": "NOW()" if answer_time is None else answer_time
            }

            self.db_connection.session.execute(sql, values)
        db.session.commit()

    def _add_survey_user_group(self, group_name, survey_id):
        """
            Helper method: Adds a survey user group for testing purposes
            Returns:
                Survey_user_groups id (UUID)
        """

        sql = """
        INSERT INTO "Survey_user_groups"
            (id, group_name, "surveyId", "createdAt", "updatedAt")
        VALUES (gen_random_uuid(), :group_name, :survey_id, NOW(), NOW())
        RETURNING id
        """
        values = {"group_name": group_name, "survey_id": survey_id}
        survey_user_group_id = self.db_connection.session.execute(
            sql, values).fetchone()[0]
        db.session.commit()
        return survey_user_group_id

    def get_count_of_user_answers_to_a_question(self,
                                                question_id,
                                                user_group_id=None,
                                                start_date=None,
                                                end_date=None,
                                                email=""):
        """
        Retrieve number of submissions to a given question.

        Args:
            survey_id: Id of survey to calculate count from
            user_group_id (optional): Filter answers by user_group. Ignored if None.
            start_date (optional): A datetime for filtering the answers used to calculate the count. Ignored
                if None. If value present only answers after this datetime are taken into account.
            end_date (optional): A datetime for filtering the answers used to calculate the count. Ignored
                if None. If value present only answers before this datetime are taken into account
            email (optional) If the user's email doesn't contain the argument, that user's answers are
                filtered out

        Returns:
            Amount of user answers if successful. Else returns 0.
        """
        # TODO:
        # Handle situation, where we want to filter in only users without any groups
        # currently group id None lists all users

        if start_date is not None and end_date is not None:
            print("not none", flush=True)
            sql = """
            SELECT COUNT(id)
            FROM "User_answers"
            WHERE "createdAt" BETWEEN :start_date AND :end_date
            AND "userId" IN (SELECT id FROM "Users" WHERE (COALESCE (email, '') LIKE :email) AND ((:group_id IS NULL) OR ("groupId" = :group_id)))
            AND "questionAnswerId" IN (
                SELECT qa.id
                FROM "Question_answers" as qa
                LEFT JOIN "User_answers" AS ua
                    ON ua."questionAnswerId" = qa.id
                WHERE qa."questionId" = :question_id
                )
            """
        else:
            print("is none", flush=True)
            sql = """
            SELECT COUNT(id)
            FROM "User_answers"
            WHERE "questionAnswerId" IN (
                SELECT qa.id
                FROM "Question_answers" as qa
                LEFT JOIN "User_answers" AS ua
                    ON ua."questionAnswerId" = qa.id
                WHERE qa."questionId" = :question_id
                AND "userId" IN (
                    SELECT id FROM "Users" WHERE (COALESCE (email, '') LIKE :email)
                        AND ((:group_id IS NULL) OR ("groupId" = :group_id))
                    ))
            """

        values = {"question_id": question_id,
                  "group_id": user_group_id,
                  "start_date": start_date,
                  "end_date": end_date,
                  "email": f"%{email}%"
                  }

        count_of_answers = self.db_connection.session.execute(sql, values).fetchone()[
            0]

        print("count_of_answers", count_of_answers, flush=True)

        if count_of_answers:
            return count_of_answers
        return 0

    def get_sum_of_user_answer_points_by_question_id(self, question_id,
                                                     user_group_id=None,
                                                     start_date=None,
                                                     end_date=None,
                                                     email=""):
        """
        Calculates the sum of the points of all the answers given to the question

        Args:
            survey_id: Id of survey to calculate sum from
            user_group_id (optional): Filter answers by user_group. Ignored if None.
            start_date (optional): A datetime for filtering the answers used to calculate the sum. Ignored
                if None. If value present only answers after this datetime are taken into account.
            end_date (optional): A datetime for filtering the answers used to calculate the sum. Ignored
                if None. If value present only answers before this datetime are taken into account.
            email (optional) If the user's email doesn't contain the argument, that user's answers are
                filtered out
        Returns:
            The sum that has been calculated
        """
        # TODO:
        # Handle situation, where we want to filter in only users without any groups
        # currently group id None lists all users
        sql = """
        SELECT
            (COUNT(ua.id) * points)
        FROM "Questions" AS q
        LEFT JOIN "Question_answers" AS qa
            ON q.id = qa."questionId"
        LEFT JOIN "User_answers" AS ua
            ON qa.id = ua."questionAnswerId"
        LEFT JOIN "Users" AS u
            ON ua."userId" = u.id
        WHERE q.id=:question_id
            AND ((:start_date IS NULL AND :end_date IS NULL) OR (ua."createdAt" BETWEEN :start_date AND :end_date))
            AND ((:group_id IS NULL) OR (u."groupId"=:group_id))
            AND (COALESCE (u.email, '') LIKE :email)
        GROUP BY q.id, qa.id
        ORDER BY q.id
        """
        values = {"question_id": question_id,
                  "group_id": user_group_id,
                  "start_date": start_date,
                  "end_date": end_date,
                  "email": f"%{email}%"}

        sum_of_points = self.db_connection.session.execute(
            sql, values).fetchall()
        db.session.commit()
        res = 0
        for i in range(0, len(sum_of_points)):
            if sum_of_points[i][0] is not None:
                res += (sum_of_points[i][0])

        return res

    def calculate_average_scores_by_category(self,
                                             survey_id,
                                             user_group_name=None,
                                             start_date=None,
                                             end_date=None,
                                             email=""):
        """
        Calculates weighted average scores from the submitted answers of a given survey. An average
        score is calculated for each category of the survey. This value represents how well all
        reponders did on each category.
        Method creates a list of tuples which contain weighted averages for all answered questions.
        A helper method is used to calculate the final category averages.
        Order of operations:
            - Get all the questions in the survey
                - For each question:
                        - Get the count of user answers [Filtered]
                        - Get the sum of user answer points [Filtered]
                        - Go through each category weight in the question
                            - For each category weight, calulate a weighted average score for the question. Append to list.
                            - If no answers are present, set weighted average score to None. Append to list.
                        - Handle the list of weighted average scores in the helper method 
        Args:
            survey_id: Id of survey to calculate averages from
            user_group_name (optional): User group name of answer. Ignored if None. If value present
                filters answers used to calculate average.
            start_date (optional): A datetime for filtering the answers used to calculate averages. Ignored
                if None. If value present only answers after this datetime are taken into account.
            end_date (optional): A datetime for filtering the answers used to calculate averages. Ignored
                if None. If value present only answers before this datetime are taken into account.
            email (optional) If the user's email doesn't contain the argument, that user's answers are
                filtered out
        Returns:
            A list of tuples which includes the category id, category name and average score
            (to the precision of two decimal places) of all user answers in a given category.
            If no answers to a category exist, the average value is contains a value of None.
        """
        # TODO:
        # Handle situation, where we want to filter in only users without any groups
        # currently group id None lists all users
        question_averages = []
        related_questions = self.repo.get_questions_of_survey(survey_id)

        for question in related_questions:

            points = self.get_sum_of_user_answer_points_by_question_id(
                question.id,user_group_name, start_date, end_date, email)

            answers = self.get_count_of_user_answers_to_a_question(
                question.id, user_group_name, start_date, end_date, email)

            for category_weight in question.category_weights:
                if answers != 0:
                    weighted_average = points / answers * \
                        category_weight['multiplier']
                else:
                    weighted_average = None
                category_id = self.repo.get_category_id_from_name(
                    survey_id, category_weight['category'])
                
                question_average = (
                        category_id, category_weight['category'], weighted_average)
                question_averages.append(question_average)

        return self.calculate_category_averages(question_averages)

    def calculate_category_averages(self, question_averages):
        """
        Helper method to calculate category averages.
        Example:
            Category A has 3 answers whose sum of weighted averages equals 10
            Category B has 2 answers whose sum of weighted averages equals 10
            Method returns the following list:
                [
                    (Category_id_A, 'Category A', 3.33),
                    (Category_id_A, 'Category A', 5.00),
                ]
        
        Each item in the question_averages list consists of:
            (category_id, category_name, weighted_average)
        Returns a list of tuples as follows:
        (category_id, category_name, category average score)
        """
        sums = {}
        occurences = {}
        names = {}
        for item in question_averages:
            if (item[2] == None):
                sums[item[0]] = None
                occurences[item[0]] = occurences.setdefault(item[0], 0)
                names[item[0]] = item[1]
            else:
                sums[item[0]] = sums.setdefault(item[0], 0) + item[2]
                occurences[item[0]] = occurences.setdefault(item[0], 0) + 1
                names[item[0]] = item[1]
        results = []
        for key in sums:
            if (sums[key] == None):
                results.append((key, names[key], None))
            else:
                results.append((key, names[key], float(
                    "{:.2f}".format(sums[key]/occurences[key]))))
        return results