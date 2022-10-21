from ast import excepthandler
import unittest

from repositories.survey_repository import SurveyRepository

from app import create_app

text = "create question test"
category_weights = '[{"category": "Category 1", "multiplier": 10.0}, {"category": "Category 2", "multiplier": 20.0}]'


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

    def test_update_survey_updated_at_changes_updated_field(self):

        with self.app.app_context():
            before = self.repo.get_survey(1)
            self.repo.update_survey_updated_at(1)
            after = self.repo.get_survey(1)
        self.assertGreater(after, before)

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

    def test_get_question_with_invalid_id_returns_none(self):

        with self.app.app_context():
            response = self.repo.get_question(99999)

        self.assertIsNone(response)

    def test_delete_survey_deletes_existing_survey(self):
        with self.app.app_context():
            survey_id = self.repo.create_survey(
                "Mock survey with little to no content",
                "in test def test_delete_survey_deletes_existing_survey(self):",
                "in survey_repository_test.py")
            self.assertTrue(self.repo.get_survey(survey_id) != False)
            self.repo.delete_survey(survey_id)
            response = self.repo.get_survey(survey_id)
        self.assertFalse(response)

    # TODO: Add functionality to this test as data becomes available.

    def test_delete_survey_deletes_related_data(self):
        with self.app.app_context():
            survey_id = self.repo.create_survey(
                "Mock survey with little to no content",
                "in test def test_delete_survey_deletes_existing_survey(self):",
                "in survey_repository_test.py")
            self.assertTrue(self.repo.get_survey(survey_id) != False)
            self.repo.delete_survey(survey_id)
            response = self.repo.get_survey(survey_id)
            get_related_questions = self.repo.get_questions_of_survey(
                survey_id)
            get_related_survey_results = []
        self.assertFalse(response)
        self.assertTrue(len(get_related_questions) == 0)
        self.assertTrue(len(get_related_survey_results) == 0)

    def test_create_question_creates_question(self):

        with self.app.app_context():

            survey_id = 1

            question_id = self.repo.create_question(
                text, survey_id, category_weights)

            result = self.repo.get_question(question_id)

        self.assertEqual(result.text, "create question test")

    def test_delete_question_from_survey_deletes_question(self):

        with self.app.app_context():
            survey_id = 1

            question_id = self.repo.create_question(
                text, survey_id, category_weights)

            response_delete = self.repo.delete_question_from_survey(
                question_id)
            response_get_deleted = self.repo.get_question(question_id)

        self.assertTrue(response_delete)
        self.assertIsNone(response_get_deleted)

    def test_delete_question_from_survey_deletes_question_answers(self):

        with self.app.app_context():
            survey_id = 1

            question_id = self.repo.create_question(
                text, survey_id, category_weights)

            for i in range(10):
                self.repo.create_answer(
                    "Test answer " + str(i), points=i*10, question_id=question_id)
            self.repo.delete_question_from_survey(
                question_id)
            response_get_answers = self.repo.get_question_answers(
                question_id)

        self.assertTrue(len(response_get_answers) == 0)

    def test_get_user_answers_returns_None_when_none_exist(self):

        with self.app.app_context():
            survey_id = 1
            question_id = self.repo.create_question(
                text, survey_id, category_weights)
            result = self.repo.get_user_answers(question_id)
        self.assertIsNone(result)

    def test_get_user_answers_returns_all_answers(self):

        with self.app.app_context():
            survey_id = 1
            question_id = self.repo.create_question(
                text, survey_id, category_weights)
            for i in range(5):
                self.repo.create_answer(
                    "Test answer " + str(i), points=i*10, question_id=question_id)
            answers = self.repo.get_question_answers(question_id)
        self.assertTrue(len(answers) == 5)
        self.assertTrue(
            answers[0][1] == "Test answer 0" and answers[4][1] == "Test answer 4")

    def test_delete_answer_from_question_deletes_answer(self):

        with self.app.app_context():
            text = "Breaking Bad"
            points = 9001
            question_id = 9

            answer_id = self.repo.create_answer(
                text, points, question_id)

            response_delete = self.repo.delete_answer_from_question(
                answer_id)
            response_get_deleted = self.repo.get_question_answers(question_id)

        self.assertTrue(response_delete)
        self.assertEqual(response_get_deleted, [])

    def test_update_question_updates_question(self):

        with self.app.app_context():
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
                "1",
                "name",
                "description",
                content_links)

        self.assertGreater(response, 0)

    def test_create_category_with_invalid_data_returns_none(self):
        with self.app.app_context():
            response = self.repo.create_category(
                "1",
                None,
                "description",
                "content_links")

        self.assertIsNone(response)

    def test_get_all_categories_returns_multiple_categories(self):
        with self.app.app_context():
            response = self.repo.get_all_categories()

        self.assertGreater(len(response), 2)

    def test_add_admin_with_invalid_data_returns_none(self):

        with self.app.app_context():
            response = self.repo.add_admin(
                {"test": "test"}
            )

        self.assertIsNone(response)

    def test_add_admin_with_valid_data_returns_id(self):

        with self.app.app_context():
            response = self.repo.add_admin("test@email.com")

        self.assertEqual(response, 9)

    def test_get_all_admins_returns_multiple_admins(self):

        with self.app.app_context():
            response = self.repo.get_all_admins()

        self.assertGreater(len(response), 1)

    def test_update_category_with_valid_data_returns_id(self):
        with self.app.app_context():
            categories = self.repo.get_all_categories()
            category_id = categories[0][0]
            name = "name"
            description = "description"
            content_links = '[{"url":"https://www.eficode.com/cases/hansen","type":"Case Study"},{"url":"https://www.eficode.com/cases/basware","type":"Case Study"}]'
            response = self.repo.update_category(
                category_id,
                "name",
                "description",
                content_links)

        self.assertGreaterEqual(response, 0)

    def test_update_category_with_invalid_data_returns_False(self):
        with self.app.app_context():
            category_id = -1
            name = "name"
            description = "description"
            content_links = '[{"url":"https://www.eficode.com/cases/hansen","type":"Case Study"},{"url":"https://www.eficode.com/cases/basware","type":"Case Study"}]'
            response = self.repo.update_category(
                category_id,
                "name",
                "description",
                content_links)
        self.assertFalse(response)

        with self.app.app_context():
            category_id = 2.5
            name = "name"
            description = "description"
            content_links = '[{"url":"https://www.eficode.com/cases/hansen","type":"Case Study"},{"url":"https://www.eficode.com/cases/basware","type":"Case Study"}]'
            response = self.repo.update_category(
                category_id,
                "name",
                "description",
                content_links)
        self.assertFalse(response)

        with self.app.app_context():
            categories = self.repo.get_all_categories()
            category_id = categories[0][0]
            name = "name"
            description = "description"
            content_links = 'abc'
            response = self.repo.update_category(
                category_id,
                "name",
                "description",
                content_links)
        self.assertFalse(response)

        with self.app.app_context():
            categories = self.repo.get_all_categories()
            category_id = categories[0][0]
            name = "name"
            description = "description"
            content_links = [{"url": "https://www.eficode.com/cases/hansen", "type": "Case Study"}, {
                "url": "https://www.eficode.com/cases/basware", "type": "Case Study"}]
            response = self.repo.update_category(
                category_id,
                "name",
                "description",
                content_links)
        self.assertFalse(response)

    def test_delete_category_deletes_existing_category(self):
        with self.app.app_context():
            content_links = '[{"url":"https://www.eficode.com/cases/hansen","type":"Case Study"},{"url":"https://www.eficode.com/cases/basware","type":"Case Study"}]'
            category_id = self.repo.create_category(
                "1",
                "name",
                "description",
                content_links)
            response1 = self.repo.delete_category(category_id)
            self.assertTrue(response1)
            response2 = self.repo.get_category(category_id)
            self.assertFalse(response2)

    def test_delete_category_with_invalid_arguments(self):
        with self.app.app_context():
            response = self.repo.delete_category('abc')
            self.assertFalse(response)

    def test_admin_exists_returns_true_when_admin_found(self):
        email = "test@gmail.com"
        with self.app.app_context():
            response = self.repo._admin_exists(email)
        self.assertTrue(response)

    def test_admin_exists_returns_false_when_admin_not_found(self):
        email = "noemail@gmail.com"
        with self.app.app_context():
            response = self.repo._admin_exists(email)
        self.assertFalse(response)
    
    def test_add_admin_does_not_add_email_if_email_found_in_db(self):
        email = "test@gmail.com"
        with self.app.app_context():
            response = self.repo.add_admin(email)
        self.assertIsNone(response)

    def test_get_categories_of_survey_returns_multiple_categories(self):
        with self.app.app_context():
            survey_id = 1
            response = self.repo.get_categories_of_survey(survey_id)

        self.assertGreater(len(response), 2)

    def test_get_categories_of_survey_returns_empty_list_if_survey_has_no_categories(self):
        with self.app.app_context():
            survey_id = 2
            response = self.repo.get_categories_of_survey(survey_id)

        self.assertEqual(len(response), 0)
