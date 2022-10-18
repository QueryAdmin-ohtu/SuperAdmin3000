import unittest
from unittest.mock import Mock
from services.survey_service import SurveyService, UserInputError


class TestSurveyService(unittest.TestCase):
    def setUp(self):
        self.repo_mock = Mock()
        self.survey_service = SurveyService(self.repo_mock)

    def test_authorized_google_login_called_with_working_email(self):
        self.repo_mock.authorized_google_login.return_value = True
        email_address = "jorma@uotinen.com"
        check = self.survey_service.check_if_authorized_google_login(
            email_address)
        self.assertTrue(check)
        self.repo_mock.authorized_google_login.assert_called_with(
            email_address)

    def test_authorized_google_login_called_with_fake_email(self):
        email_address = "jorma@uotinennet"
        check = self.survey_service.check_if_authorized_google_login(
            email_address)
        self.assertFalse(check)
        assert not self.repo_mock.authorized_google_login.called

    def test_create_survey_works_with_proper_arguments(self):
        self.repo_mock.create_survey.return_value = 1
        name = "Marsupial Survey"
        title = "What marsupial woudl I be?"
        description = "Come and find out what marsupial represents you best"
        check = self.survey_service.create_survey(name, title, description)
        self.assertEqual(check, 1)
        self.repo_mock.create_survey.assert_called_with(
            name, title, description)

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
        survey_to_return = {"name": "survey_name",
                            "title": "survey_title", "description": "survey_description"}
        survey_id = 1
        self.repo_mock.get_survey.return_value = survey_to_return
        check = self.survey_service.get_survey(survey_id)
        self.assertEqual(check, survey_to_return)
        self.repo_mock.get_survey.assert_called_with(survey_id)

    def test_get_all_surveys_calls_repo_correctly(self):
        surveys_to_return = [{"name": "survey_name", "title": "survey_title",
                              "description": "survey_description", "questions": 12, "submissions": 2}]
        self.repo_mock.get_all_surveys.return_value = surveys_to_return
        check = self.survey_service.get_all_surveys()
        self.assertEqual(surveys_to_return, check)
        self.repo_mock.get_all_surveys.assert_called_once()

    def test_get_questions_of_survey_calls_repo_correctly(self):
        questions_to_return = ["question1", "question2"]
        survey_id = 1
        self.repo_mock.get_questions_of_survey.return_value = questions_to_return
        check = self.survey_service.get_questions_of_survey(survey_id)
        self.assertEqual(questions_to_return, check)
        self.repo_mock.get_questions_of_survey.assert_called_with(survey_id)

    def test_get_question_answers_calls_repo_correctly(self):
        answers_to_return = ["because", 44]
        question_id = 10
        self.repo_mock.get_question_answers.return_value = answers_to_return
        check = self.survey_service.get_question_answers(question_id)
        self.assertEqual(answers_to_return, check)
        self.repo_mock.get_question_answers.assert_called_with(question_id)

    def test_get_all_categories_calls_repo_correctly(self):
        categories_to_return = ["id", "name", "description", "content_links"]
        self.repo_mock.get_all_categories.return_value = categories_to_return
        check = self.survey_service.get_all_categories()
        self.assertEqual(categories_to_return, check)
        self.repo_mock.get_all_categories.assert_called_once()

    def test_create_question_calls_repo_correctly(self):
        self.repo_mock.create_question.return_value = 1
        text = "text"
        survey_id = 1
        category_weights = []
        check = self.survey_service.create_question(
            text, survey_id, category_weights)
        self.assertEqual(check, 1)
        self.repo_mock.create_question.assert_called_with(
            text, survey_id, category_weights)

    def test_create_answer_calls_repo_correctly(self):
        self.repo_mock.create_answer.return_value = 9
        text = "Breaking Bad"
        question_id = 9
        points = 9001
        check = self.survey_service.create_answer(
            text, points, question_id)
        self.assertEqual(check, 9)
        self.repo_mock.create_answer.assert_called_with(
            text, points, question_id)

    def test_edit_survey_with_no_name_does_not_work(self):
        name = ""
        title = "What marsupial woudl I be?"
        description = "Come and find out what marsupial represents you best"
        with self.assertRaises(UserInputError):
            self.survey_service.edit_survey(1, name, title, description)

    def test_edit_survey_works_with_proper_arguments(self):
        self.repo_mock.edit_survey.return_value = 1
        id = "1"
        name = "Marsupial Survey"
        title = "What marsupial woudl I be?"
        description = "Come and find out what marsupial represents you best"
        check = self.survey_service.edit_survey(id, name, title, description)
        self.assertEqual(check, 1)
        self.repo_mock.edit_survey.assert_called_with(
            id, name, title, description)

    def test_edit_survey_with_no_title_does_not_work(self):
        id = "1"
        name = "Marsupial Survey"
        title = ""
        description = "Come and find out what marsupial represents you best"
        with self.assertRaises(UserInputError):
            self.survey_service.edit_survey(id, name, title, description)

    def test_edit_survey_with_no_description_does_not_work(self):
        id = "1"
        name = "Marsupial Survey"
        title = "What marsupial woudl I be?"
        description = ""
        with self.assertRaises(UserInputError):
            self.survey_service.edit_survey(id, name, title, description)

    def test_update_question_calls_repo_correctly(self):
        self.repo_mock.update_question.return_value = 1
        text = "change"
        question_id = 6
        category_weights = []
        check = self.survey_service.update_question(
            question_id, text, category_weights)
        self.assertEqual(check, 1)
        self.repo_mock.update_question.assert_called_with(
            question_id, text, category_weights)

    def test_create_category_calls_repo_correctly(self):
        self.repo_mock.create_category.return_value = 1
        survey_id="1"
        name = "name"
        description = "description"
        content_links = [{"url": "https://www.eficode.com/cases/hansen", "type": "Case Study"},
                         {"url": "https://www.eficode.com/cases/basware", "type": "Case Study"}]
        check = self.survey_service.create_category(
            survey_id, name, description, content_links)
        self.assertEqual(check, 1)
        self.repo_mock.create_category.assert_called_with(
            survey_id, name, description, content_links)

    def test_add_admin_calls_repo_correctly(self):
        self.repo_mock.add_admin.return_value = 1
        email = "jorma@uotinen.net"
        check = self.survey_service.add_admin(
            email)
        self.assertEqual(check, 1)
        self.repo_mock.add_admin.assert_called_with(
            email)

    def test_add_admin_without_valid_email_returns_none(self):
        email = "jorma@uotinennet"
        check = self.survey_service.add_admin(email)
        self.assertIsNone(check)

    def test_get_all_admins_calls_repo_correctly(self):
        self.repo_mock.get_all_admins.return_value = [
            ("1", "jorma@uotinen.net"),
            ("2", "uotinen@jorma.fi")]
        check = self.survey_service.get_all_admins()
        self.assertEqual(check,
                         [
                             ("1", "jorma@uotinen.net"),
                             ("2", "uotinen@jorma.fi")])
        self.repo_mock.get_all_admins.assert_called()

    def test_update_category_calls_repo_correctly(self):
        self.repo_mock.update_category.return_value = 1
        category_id = 0
        name = "name"
        description = "description"
        content_links = [{"url": "https://www.eficode.com/cases/hansen", "type": "Case Study"},
                         {"url": "https://www.eficode.com/cases/basware", "type": "Case Study"}]
        check = self.survey_service.update_category(
            category_id, name, description, content_links)
        self.assertEqual(check, 1)
        self.repo_mock.update_category.assert_called_with(
            category_id, name, description, content_links)

    def test_delete_category_calls_repo_correctly(self):
        self.repo_mock.delete_category.return_value = 1
        category_id = 0
        check = self.survey_service.delete_category(category_id)
        self.assertEqual(check, 1)
        self.repo_mock.delete_category.assert_called_with(category_id)

    def test_get_category_calls_repo_correctly(self):
        self.repo_mock.get_category.return_value = 1
        category_id = 0
        check = self.survey_service.get_category(category_id)
        self.assertEqual(check, 1)
        self.repo_mock.get_category.assert_called_with(category_id)

    def test_get_categories_of_survey_calls_repo_correctly(self):
        return_value=["1", "nimi", "kuvaus", []]
        self.repo_mock.get_categories_of_survey.return_value = return_value
        survey_id = 1
        check = self.survey_service.get_categories_of_survey(survey_id)
        self.assertEqual(check, return_value)
        self.repo_mock.get_categories_of_survey.assert_called_with(survey_id)