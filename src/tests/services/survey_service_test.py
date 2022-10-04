import unittest
from unittest.mock import Mock
from datetime import datetime
from freezegun import freeze_time
from services.survey_service import SurveyService, UserInputError

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

    # SurveyService assigns the current time to each survey. @freeze_time allows us to set the current
    # datetime.now() time for tests
    @freeze_time('2013-04-09') 
    def test_create_survey_works_with_proper_arguments(self):
        self.repo_mock.create_survey.return_value = 1
        name = "Marsupial Survey"
        title = "What marsupial woudl I be?"
        description = "Come and find out what marsupial represents you best"
        check = self.survey_service.create_survey(name, title, description)
        self.assertEqual(check, 1)
        self.repo_mock.create_survey.assert_called_with(name, title, description, datetime(2013, 4, 9))

    def test_create_survey_with_no_name_does_not_work(self):
        name = ""
        title = "What marsupial woudl I be?"
        description = "Come and find out what marsupial represents you best"
        with self.assertRaises(UserInputError):
            self.survey_service.create_survey(name, title, description)

    def test_create_survey_with_no_title_does_not_work(self):
        name = "Marsupial Survey"
        title = ""
        description = "Come and find out what marsupial represents you best"
        with self.assertRaises(UserInputError):
            self.survey_service.create_survey(name, title, description)

    def test_create_survey_with_no_description_does_not_work(self):
        name = "Marsupial Survey"
        title = "What marsupial woudl I be?"
        description = ""
        with self.assertRaises(UserInputError):
            self.survey_service.create_survey(name, title, description)

    def test_get_survey_calls_repo_correctly(self):
        survey_to_return = { "name": "survey_name" , "title": "survey_title", "description": "survey_description" }
        survey_id = 1
        self.repo_mock.get_survey.return_value = survey_to_return
        check = self.survey_service.get_survey(survey_id)
        self.assertEqual(check, survey_to_return)
        self.repo_mock.get_survey.assert_called_with(survey_id)

    def test_get_all_surveys_calls_repo_correctly(self):
        surveys_to_return = [{"name": "survey_name" , "title": "survey_title", "description": "survey_description", "questions": 12, "submissions": 2}]
        self.repo_mock.get_all_surveys.return_value = surveys_to_return
        check = self.survey_service.get_all_surveys()
        self.assertEqual(surveys_to_return, check)
        self.repo_mock.get_all_surveys.assert_called_once()

    def test_get_questions_of_survey_calls_repo_correctyl(self):
        questions_to_return= ["question1", "question2"]
        survey_id = 1
        self.repo_mock.get_questions_of_survey.return_value = questions_to_return
        check = self.survey_service.get_questions_of_survey(survey_id)
        self.assertEqual(questions_to_return, check)
        self.repo_mock.get_questions_of_survey.assert_called_with(survey_id)