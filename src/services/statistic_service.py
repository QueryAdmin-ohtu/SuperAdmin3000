from repositories.statistic_repository import StatisticRepository
from datetime import datetime

class UserInputError(Exception):
    pass


class StatisticService:
    """
    A class for safely interacting with the survey repository
    """

    def __init__(self, statistic_repository):
        self.statistic_repository = statistic_repository


    def get_number_of_submissions_for_survey(self, survey_id):
        """
        Fetches the number of submissions for the given
        survey

        Returns:
        Number of submissions as integer
        """

        return self.statistic_repository.get_number_of_submissions(survey_id)

    def get_answer_distribution_for_survey_questions(self,
                                                     survey_id,
                                                     start_date: datetime = None,
                                                     end_date: datetime = None,
                                                     group_id=None,
                                                     email: str = ""):
        """
        Fetches the distribution of user answers over the
        answer options of a survey. Checks if there are user answers.

        Args:
            survey_id   The id of the survey
            start_date  Filter out answers before this date (optional)
            end_date    Filter out answers after this date (optional)
            group_id    Filter out answers from users not in this group (optional)
            email       Filter in answers from users whose email matches (optional)

        Returns: a list of sqlalchemy.engine.row.Row objects: fields question_id, question,
        answer_id, answer, count (of user answers);
        None if there are no user answers
        """

        result = self.statistic_repository.get_answer_distribution(survey_id,
                                                                start_date,
                                                                end_date,
                                                                group_id,
                                                                email)

        if not result:
            return None
        if self._user_submissions(result):
            return result
        return None

    def _user_submissions(self, answer_distribution):
        """
        Check if there are user submissions in a set of answer distribution

        Returns boolean
        """
        for question in answer_distribution:
            if question.count > 0:
                return True
        return False

    def get_count_of_user_answers_to_a_question(self, question_id):
        """
        Fetches and returns the number of user answers to a given question id
        """

        return self.statistic_repository.get_count_of_user_answers_to_a_question(question_id)

    def get_sum_of_user_answer_points_by_question_id(self, question_id):
        """
        Fetches and returns the sum of user answer points to a given question id
        """
        return self.statistic_repository.get_sum_of_user_answer_points_by_question_id(question_id)

    def calculate_average_scores_by_category(self,
                                             survey_id,
                                             user_group_id=None,
                                             start_date=None,
                                             end_date=None,
                                             email=""):
        """
        Calculates weighted average scores from the submitted answers of a given survey. An average
        score is calculated for each category of the survey. This value represents how well all
        reponders did on each category.

        Method creates a list of tuples which contain weighted averages for all answered questions.
        A helper method is used to calculate the final category averages.

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
            A list of tuples which includes the category id, category name, average score and
            average score for unfiltered results
            (to the precision of two decimal places) of all user answers in a given survey.
            (id, name, average, average_of_all)

            If dates invalid returns None
        """

        if start_date and end_date:
            if start_date > end_date or end_date < start_date:
                return None

        all_averages = self.statistic_repository.calculate_average_scores_by_category(
            survey_id)
        filtered_averages = self.statistic_repository.calculate_average_scores_by_category(
            survey_id, user_group_id, start_date, end_date, email)

        result = []

        for average in filtered_averages:
            for a in all_averages:
                if a[0] == average[0]:  # Matching id
                    average_of_all = a[2]
                    break
            else:
                average_of_all = None
            result.append(average + (average_of_all,))

        return result

    def get_users_who_answered_survey(self, survey_id: int):
        """ Returns a list of users who have answered a given survey
        Args:
            survey_id: Id of the survey

        Returns:
            On succeed: A list of lists where each element contains
                [id, email, group_id, group_name, answer_time]
            On error / no users who answered found:
                None
        """
        return self.statistic_repository.get_users_who_answered_survey(survey_id)

    def get_users_who_answered_survey_filtered(self,
                                               survey_id: int,
                                               start_date: datetime,
                                               end_date: datetime,
                                               group_id,
                                               email):
        """ Returns a list of users who have answered a given survey in a given timerange,
        belonging the given group and having a matching email address
        Args:
           survey_id: Id of the survey
           start_time: Start of timerange to filter by
           end_time: End of timerange to filter by
           group_name: Name of the user group to filter by
           email: Email address to filter by

        Returns:
           On succeed: A list of lists where each element contains
               [id, email, group_id, group_name, answer_time]
           On error / no users who answered found:
               None
        """

        if start_date > end_date or end_date < start_date:
            return None

        return self.statistic_repository.get_users_who_answered_survey(survey_id,
                                                                    start_date,
                                                                    end_date,
                                                                    group_id,
                                                                    email)

    def get_users_who_answered_survey_in_timerange(self, survey_id: int, start_date: datetime, end_date: datetime):
        """ Returns a list of users who have answered a given survey in a given timerange
        Args:
            survey_id: Id of the survey
            start_time: Start of timerange to filter by
            end_time: End of timerange to filter by

        Returns:
            On succeed: A list of lists where each element contains
                [id, email, group_name, answer_time]
            On error / no users who answered found:
                None
        """

        if start_date > end_date or end_date < start_date:
            # Invalid timerange
            return None

        return self.statistic_repository.get_users_who_answered_survey(survey_id, start_date, end_date)

    def get_users_who_answered_survey_in_group(self, survey_id: int, group_name):
        """ Returns a list of users who have answered a given survey in a given timerange
        Args:
            survey_id: Id of the survey
            group_name: Name of the user group to filter by
        Returns:
            On succeed: A list of lists where each element contains
                [id, email, group_name, answer_time]
            On error / no users who answered found:
                None
        """

        return self.statistic_repository.get_users_who_answered_survey(survey_id, group_name=group_name)


statistic_service = StatisticService(StatisticRepository())
