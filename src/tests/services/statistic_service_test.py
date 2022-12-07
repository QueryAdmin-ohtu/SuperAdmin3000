import unittest
from datetime import datetime
from unittest.mock import Mock
from services.statistic_service import StatisticService


class TestSurveyService(unittest.TestCase):
    def setUp(self):
        self.repo_mock = Mock()
        self.statistic_service = StatisticService(self.repo_mock)
        self.start_date = datetime.fromisoformat("2011-10-04 00:00:21.283")
        self.end_date = datetime.fromisoformat("2012-10-04 00:00:21.283")

    def test_calculate_average_scores_by_category_calls_repo_correctly(self):
        self.repo_mock.calculate_average_scores_by_category.return_value = [(1, "Category Name", None)]
        start_date = datetime.fromisoformat("2011-10-04 00:00:21.283")
        end_date = datetime.fromisoformat("2012-10-04 00:00:21.283")
        response = self.statistic_service.calculate_average_scores_by_category(1, None, start_date, end_date, "")
        self.repo_mock.calculate_average_scores_by_category.assert_called_with(1, None, start_date, end_date, "")
        self.assertEquals(response, [(1, "Category Name", None, None)])

    def test_get_number_of_submissions(self):
        self.repo_mock.get_number_of_submissions.return_value = 1
        response = self.statistic_service.get_number_of_submissions_for_survey(1)
        self.assertEquals(response, 1)

    def test_get_answer_distribution_returns_none(self):
        self.repo_mock.get_answer_distribution.return_value = None
        response = self.statistic_service.get_answer_distribution_for_survey_questions(1)
        self.assertEquals(response, None)

    def test_get_sum_of_user_answer_points_calls_repo_correctly(self):
        self.repo_mock.get_sum_of_user_answer_points_by_question_id.return_value = 3
        response = self.statistic_service.get_sum_of_user_answer_points_by_question_id(3)
        self.assertEquals(response, 3)

    def test_get_users_who_answered_survey_calls_repo_correctly(self):
        self.repo_mock.get_users_who_answered_survey.return_value = [[1,"user@domain.invalid", 'bb2ce58d-f27b-4ade-9e31-e8aca8c7ca20', 'Group Name', self.start_date]]
        response = self.statistic_service.get_users_who_answered_survey(1)
        self.assertEquals(response, [[1,"user@domain.invalid", 'bb2ce58d-f27b-4ade-9e31-e8aca8c7ca20', 'Group Name', self.start_date]])

    def test_get_users_who_answered_survey_with_invalid_timerange_returns_none(self):
        response = self.statistic_service.get_users_who_answered_survey_filtered(1, self.end_date, self.start_date, "Null", "")
        self.assertEquals(response, None)

    def test_get_count_of_user_answers_returns_correctly(self):
        self.repo_mock.get_count_of_user_answers_to_a_question.return_value = 2
        response = self.statistic_service.get_count_of_user_answers_to_a_question(2)
        self.assertEqual(response, 2)

    def test_get_users_who_answered_survey_in_timerange_invalid(self):
        response = self.statistic_service.get_users_who_answered_survey_in_timerange(1, self.end_date, self.start_date)
        self.assertEquals(response, None)