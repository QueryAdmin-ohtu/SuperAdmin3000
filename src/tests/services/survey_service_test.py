import unittest
from unittest.mock import Mock

from services.survey_service import SurveyService

from datetime import datetime

class TestSurveyService(unittest.TestCase):
    def setUp(self):
        self.repo_mock = Mock()
        self.survey_service = SurveyService(self.repo_mock)

    def test_authorized_google_login_called_with_working_email(self):
        self.repo_mock.authorized_google_login.return_value = True
        email_address = "jorma@uotinen.com"
        check = self.survey_service.check_if_authorized_google_login(email_address)
        self.assertTrue(check)
        self.repo_mock.authorized_google_login.assert_called_with(email_address)

    def test_authorized_google_login_called_with_fake_email(self):
        email_address = "jorma@uotinencom"
        check = self.survey_service.check_if_authorized_google_login(email_address)
        self.assertFalse(check)
        assert not self.repo_mock.authorized_google_login.called
        
    def test_create_survey_works_with_proper_arguments(self):
        self.repo_mock.create_survey.return_value = 1
        name = "Marsupial Survey"
        title = "What marsupial woudl I be?"
        description = "Come and find out what marsupial represents you best"
        check = self.survey_service.create_survey(name, title, description)
        self.assertEqual(check, 1)
        self.repo_mock.create_survey.assert_called_with(name, title, description, datetime.now)
