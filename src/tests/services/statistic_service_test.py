import unittest
from datetime import datetime
from unittest.mock import Mock
from services.statistic_service import StatisticService


class TestSurveyService(unittest.TestCase):
    def setUp(self):
        self.repo_mock = Mock()
        self.statistic_service = StatisticService(self.repo_mock)


    def test_calculate_average_scores_by_category_calls_repo_correctly(self):
        self.repo_mock.calculate_average_scores_by_category.return_value = [(1, "Category Name", None)]
        start_date = datetime.fromisoformat("2011-10-04 00:00:21.283")
        end_date = datetime.fromisoformat("2012-10-04 00:00:21.283")
        response = self.statistic_service.calculate_average_scores_by_category(1, None, start_date, end_date, "")
        self.repo_mock.calculate_average_scores_by_category.assert_called_with(1, None, start_date, end_date, "")
        self.assertEquals(response, [(1, "Category Name", None, None)])
