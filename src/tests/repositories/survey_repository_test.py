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

    def test_get_question_returns_question(self):
        with self.app.app_context():
            response = self.repo.get_questions_of_survey(1)

        self.assertGreater(len(response), 2)

    def test_get_question_with_invalid_id_returns_none(self):

        with self.app.app_context():
            response = self.repo.get_question(99999)

        self.assertIsNone(response)

    def test_delete_survey_deletes_existing_survey(self):

        with self.app.app_context():
            self.repo.delete_survey(2)
            response = self.repo.get_survey(2)

        self.assertFalse(response)

    def test_create_question_creates_question(self):

        with self.app.app_context():
            text = "create question test"
            survey_id = 1
            category_weights = '[{"category": "Category 1", "multiplier": 10.0}, {"category": "Category 2", "multiplier": 20.0}]'
            created = datetime.now()

            question_id = self.repo.create_question(
                text, survey_id, category_weights, created)

            result = self.repo.get_question(question_id)

        self.assertEqual(result.text, "create question test")

    def test_delete_question_from_survey_deletes_question(self):

        with self.app.app_context():
            text = "create question test"
            survey_id = 1
            category_weights = '[{"category": "Category 1", "multiplier": 10.0}, {"category": "Category 2", "multiplier": 20.0}]'
            created = datetime.now()

            question_id = self.repo.create_question(
                text, survey_id, category_weights, created)

            response_delete = self.repo.delete_question_from_survey(
                question_id)
            response_get_deleted = self.repo.get_question(question_id)

        self.assertTrue(response_delete)
        self.assertIsNone(response_get_deleted)

    def test_update_question_updates_question(self):

        with self.app.app_context():
            text = "create question test"
            survey_id = 1
            category_weights = '[{"category": "Category 1", "multiplier": 10.0}, {"category": "Category 2", "multiplier": 20.0}]'
            created = datetime.now()

            question_id = self.repo.create_question(
                text, survey_id, category_weights, created)

            new_text = "update question test"
            updated = datetime.now()

            result_update = self.repo.update_question(
                question_id, new_text, category_weights, updated)

            result_get_new = self.repo.get_question(question_id)

        self.assertTrue(result_update)
        self.assertEqual(result_get_new.text, "update question test")
