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

        with self.app.app_context():
            response = self.repo.create_survey(
                "name",
                "title",
                "text")

        self.assertGreater(response, 0)

    def test_create_survey_with_invalid_data_returns_none(self):

        with self.app.app_context():
            response = self.repo.create_survey(
                None,
                "title",
                "text")

        self.assertIsNone(response)

    def test_survey_with_the_same_name_exists(self):
        with self.app.app_context():
            self.repo.create_survey(
                "MDZS",
                "Rejoice!",
                "WWX is dead!"
            )
            response = self.repo.survey_exists("mdzs")

            self.assertTrue(response)

    def test_survey_with_the_same_name_doesnt_exist(self):
        with self.app.app_context():
            response = self.repo.survey_exists("totally nonexistent survey")
            self.assertFalse(response)

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

    def test_get_answers_of_question_returns_questions(self):

        with self.app.app_context():
            response = self.repo.get_question_answers(2)
        self.assertGreater(len(response), 0)

    def test_edit_survey_returns_none_with_invalid_arguments(self):

        with self.app.app_context():
            response = self.repo.edit_survey(
                None,
                "name_test",
                "title_test",
                "description_test"
            )

        self.assertIsNone(response)

    def test_edit_survey_returns_id_with_valid_arguments(self):

        with self.app.app_context():
            response = self.repo.edit_survey(
                "1",
                "name_test",
                "title_test",
                "description_test"
            )

        self.assertEqual(response, 1)

    def test_edit_survey_returns_false_with_invalid_input(self):

        with self.app.app_context():
            response = self.repo.edit_survey(
                "one",
                "mame_test",
                "title_test",
                "description_test"
            )

        self.assertFalse(response)

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

            question_id = self.repo.create_question(
                text, survey_id, category_weights)

            result = self.repo.get_question(question_id)

        self.assertEqual(result.text, "create question test")

    def test_delete_question_from_survey_deletes_question(self):

        with self.app.app_context():
            text = "create question test"
            survey_id = 1
            category_weights = '[{"category": "Category 1", "multiplier": 10.0}, {"category": "Category 2", "multiplier": 20.0}]'

            question_id = self.repo.create_question(
                text, survey_id, category_weights)

            response_delete = self.repo.delete_question_from_survey(
                question_id)
            response_get_deleted = self.repo.get_question(question_id)

        self.assertTrue(response_delete)
        self.assertIsNone(response_get_deleted)

    def test_delete_answer_from_question_deletes_answer(self):

        with self.app.app_context():
            question_id = 2
            answer_id = 10
            response_delete = self.repo.delete_answer_from_question(
                answer_id)
            response_get_deleted = self.repo.get_question_answers(question_id)

        self.assertTrue(response_delete)
        self.assertEqual(len(response_get_deleted),4)

    def test_update_question_updates_question(self):

        with self.app.app_context():
            text = "create question test"
            survey_id = 1
            category_weights = '[{"category": "Category 1", "multiplier": 10.0}, {"category": "Category 2", "multiplier": 20.0}]'

            question_id = self.repo.create_question(
                text, survey_id, category_weights)

            new_text = "update question test"

            result_update = self.repo.update_question(
                question_id, new_text, category_weights)

            result_get_new = self.repo.get_question(question_id)

        self.assertTrue(result_update)
        self.assertEqual(result_get_new.text, "update question test")

    def test_create_category_with_valid_data_returns_id(self):
        content_links = '[{"url":"https://www.eficode.com/cases/hansen","type":"Case Study"},{"url":"https://www.eficode.com/cases/basware","type":"Case Study"}]'

        with self.app.app_context():
            response = self.repo.create_category(
                "name",
                "description",
                content_links)

        self.assertGreater(response, 0)

    def test_create_category_with_invalid_data_returns_none(self):

        with self.app.app_context():
            response = self.repo.create_category(
                None,
                "description",
                "content_links")

        self.assertIsNone(response)

    def test_get_all_categories_returns_multiple_categories(self):

        with self.app.app_context():
            response = self.repo.get_all_categories()

        self.assertGreater(len(response), 2)
            