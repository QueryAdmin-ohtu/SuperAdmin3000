import unittest
from datetime import datetime

from repositories.survey_repository import SurveyRepository

from app import create_app


class TestSurveyRepository(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.repo = SurveyRepository()

    def test_authorized_google_login_with_valid_email_succeeds(self):
        
        valid_email = "jatufin@gmail.com"

        with self.app.app_context():
            response = self.repo.authorized_google_login(valid_email)
        
        self.assertTrue(response)

    def test_authorized_google_login_with_invalid_email_fails(self):
        
        valid_email = "jatufin@gmail.invalid"

        with self.app.app_context():
            response = self.repo.authorized_google_login(valid_email)
        
        self.assertFalse(response)

    def test_create_survey_with_valid_data_returns_id(self):
        name = "name"
        title = "title"
        text = "text"
        createdAt = datetime.now()
        
        with self.app.app_context():
            response = self.repo.create_survey(
                "name",
                "title",
                "text",
                datetime.now())
        
        self.assertGreater(response, 0)

    def test_create_survey_with_invalid_data_returns_none(self):
        
        with self.app.app_context():
            response = self.repo.create_survey(
                None,
                "title",
                "text",
                datetime.now())
        
        self.assertIsNone(response)

    def test_get_survey_with_valid_id_returns_survey(self):

        with self.app.app_context():
            response = self.repo.get_survey(1)
        
        self.assertIsNotNone(response)

    def test_get_survey_with_invalid_id_returns_false(self):

        with self.app.app_context():
            response = self.repo.get_survey(999999)
        
        self.assertFalse(response)

    def test_get_all_surveys_calls_returns_multiple_surveys(self):

        with self.app.app_context():
            response = self.repo.get_all_surveys()
        
        self.assertGreater(len(response), 2) 

    def test_get_questions_of_survey_returns_questions(self):

        with self.app.app_context():
            response = self.repo.get_questions_of_survey(1)
        
        self.assertGreater(len(response), 2) 
