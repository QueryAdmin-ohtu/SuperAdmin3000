import unittest
from datetime import datetime
from collections import namedtuple
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
        self.repo_mock.create_survey_result.assert_called_with(
            1,
            "Your skills in this topic are excellent!",
            1.0
        )

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
        surveys_to_return = [[1, "title1", 12, 2],
                             [2, "title2", 5, 10]]

        survey_status_array = ["red", False, True, [], True, [], [], [], {}]

        self.repo_mock.get_all_surveys.return_value = surveys_to_return
        self.repo_mock.check_survey_status.return_value = survey_status_array

        survey_status_to_expect = {
            "status_color": survey_status_array[0],
            "no_survey_results": survey_status_array[1],
            "no_categories": survey_status_array[2],
            "unrelated_categories_in_weights": survey_status_array[3],
            "no_questions": survey_status_array[4],
            "questions_without_answers": survey_status_array[5],
            "questions_without_categories": survey_status_array[6],
            "categories_without_questions": survey_status_array[7],
            "categories_without_results": {}
        }

        surveys_with_status = [[1, "title1", 12, 2, survey_status_to_expect],
                               [2, "title2", 5, 10, survey_status_to_expect]]

        
        result = self.survey_service.get_all_surveys()

        self.assertEqual(surveys_with_status, result)
        self.repo_mock.check_survey_status.assert_called_with(2)
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
            question_id, text, category_weights, [], [])
        self.assertEqual(check, 1)
        self.repo_mock.update_question.assert_called_with(
            question_id, text, category_weights, [], [])

    def test_create_category_calls_repo_correctly(self):
        self.repo_mock.create_category.return_value = 1
        survey_id = "1"
        category_id = "1"
        name = "name"
        description = "description"
        content_links = [{"url": "https://www.eficode.com/cases/hansen", "type": "Case Study"},
                         {"url": "https://www.eficode.com/cases/basware", "type": "Case Study"}]
        check = self.survey_service.create_category(
            survey_id, name, description, content_links)
        self.assertEqual(check, 1)
        self.repo_mock.create_category.assert_called_with(
            survey_id, name, description, content_links)
        self.repo_mock.create_category_result.called_with(
            1,
            1,
            "Your skills in this topic are excellent!",
            1.0
        )

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
            category_id, content_links, name, description, )
        self.assertEqual(check, 1)
        self.repo_mock.update_category.assert_called_with(
            category_id, content_links, name, description)

    def test_update_category_calls_repo_correctly_without_name_and_description(self):
        self.repo_mock.get_category.return_value = (1,
                                                    'Category 1',
                                                    'Static descriptive text about the category 1.',
                                                    [{'url': 'https://www.eficode.com/cases/hansen', 'type': 'Case Study'}, {
                                                        'url': 'https://www.eficode.com/cases/basware', 'type': 'Case Study'}],
                                                    'created_time_here',
                                                    'updated_time_here',
                                                    1)
        category_id = 0
        content_links = [{"url": "https://www.eficode.com/cases/hansen", "type": "Case Study"},
                         {"url": "https://www.eficode.com/cases/basware", "type": "Case Study"}]
        self.survey_service.update_category(
            category_id, content_links)
        name = self.repo_mock.get_category(category_id)[1]
        description = self.repo_mock.get_category(category_id)[2]
        self.repo_mock.update_category.assert_called_with(
            category_id, content_links, name, description)

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
        return_value = ["1", "nimi", "kuvaus", []]
        self.repo_mock.get_categories_of_survey.return_value = return_value
        survey_id = 1
        check = self.survey_service.get_categories_of_survey(survey_id)
        self.assertEqual(check, return_value)
        self.repo_mock.get_categories_of_survey.assert_called_with(survey_id)

    def test_get_user_answers_calls_repo_correctly(self):
        return_values = [(1, "Test answer 1", 5), (2, "Test answer 2", 7)]
        self.repo_mock.get_user_answers.return_value = return_values
        question_id = 1
        check = self.survey_service.get_user_answers(question_id)
        self.assertEqual(check, return_values)
        self.repo_mock.get_user_answers.assert_called_with(question_id)

    def test_delete_question_calls_repo_correctly(self):
        return_value = True
        self.repo_mock.delete_question_from_survey.return_value = return_value
        question_id = 1
        check = self.survey_service.delete_question_from_survey(question_id)
        self.repo_mock.delete_question_from_survey.assert_called_with(
            question_id)
        self.assertEqual(check, return_value)

    def test_create_category_result_calls_repo_correctly(self):
        self.repo_mock.create_category_result.return_value = 1
        category_id = 1
        survey_id = 1
        text = "Dynamically fetched category result text"
        cutoff_from_maxpts = 1.0
        response = self.survey_service.create_category_result(
            category_id,
            survey_id,
            text,
            cutoff_from_maxpts)
        self.assertEqual(response, category_id)
        self.repo_mock.create_category_result.assert_called_with(
            category_id,
            text,
            cutoff_from_maxpts)

    def test_get_survey_results_calls_repo_correctly(self):
        self.repo_mock.get_survey_results.return_value = [
            15, "You are very mature and agile", 1.0]
        response = self.survey_service.get_survey_results(1)
        self.assertEqual(response[0], 15)
        self.repo_mock.get_survey_results.assert_called_with(1)

    def test_create_survey_result_calls_repo_correctly(self):
        self.repo_mock.create_survey_result.return_value = 15
        response = self.survey_service.create_survey_result(
            1, "You are very mature and agile!", 0.9)
        self.assertEqual(response, 15)
        self.repo_mock.create_survey_result.assert_called_with(
            1, "You are very mature and agile!", 0.9)

    def test_delete_survey_result_calls_repo_correctly(self):
        self.repo_mock.delete_survey_result.return_value = True

        response = self.survey_service.delete_survey_result(1)
        self.assertTrue(response)
        self.repo_mock.delete_survey_result.assert_called_with(1)

    def test_update_survey_results_calls_repo_correctly(self):
        self.repo_mock.delete_survey_result.return_value = True
        original_results = [[5, "Bad", 0.3], [6, "Good", 1.0]]
        new_results = [[5, "Decent", 0.3], [6, "Great", 1.0]]
        response = self.survey_service.update_survey_results(original_results,
                                                             new_results, 3)
        self.assertTrue(response)
        self.repo_mock.update_survey_results.assert_called_with(original_results,
                                                                new_results, 3)

    def test_delete_category_result_calls_repo_correctly(self):
        self.repo_mock.delete_category_result.return_value = True
        response = self.survey_service.delete_category_result(1, 1, 1)
        self.assertTrue(response)
        self.repo_mock.delete_category_result.assert_called_with(1)

    def test_update_category_results_calls_repo_correctly(self):
        self.repo_mock.delete_survey_result.return_value = True
        original_results = [[5, "Bad", 0.3], [6, "Good", 1.0]]
        new_results = [[5, "Decent", 0.3], [6, "Great", 1.0]]
        response = self.survey_service.update_category_results(original_results,
                                                               new_results, 3, 1)
        self.assertTrue(response)
        self.repo_mock.update_category_results.assert_called_with(original_results,
                                                                  new_results, 3)

    def test_check_survey_status_calls_repo_correctly(self):

        survey_status_array = ["red", False, True, [], True, [], [], [], {}]
        self.repo_mock.check_survey_status.return_value = survey_status_array

        survey_status_to_expect = {
            "status_color": survey_status_array[0],
            "no_survey_results": survey_status_array[1],
            "no_categories": survey_status_array[2],
            "unrelated_categories_in_weights": survey_status_array[3],
            "no_questions": survey_status_array[4],
            "questions_without_answers": survey_status_array[5],
            "questions_without_categories": survey_status_array[6],
            "categories_without_questions": survey_status_array[7],
            "categories_without_results": {}
        }

        returned_value = self.survey_service.check_survey_status(1)
        self.repo_mock.check_survey_status.assert_called_with(1)
        self.assertEquals(survey_status_to_expect, returned_value)

    def test_delete_category_in_questions_calls_repo_correctly(self):
        self.repo_mock.remove_category_from_question.return_value = "test"
        question_ids = [1, 2, 3]
        questions_weights = ['[{"category": "Koira", "multiplier": 5.0}, {"category": "Cat", "multiplier": -5.0}]',
                             '[{"category": "Koira", "multiplier": 5.0}, {"category": "Cat", "multiplier": -5.0}]',
                             '[{"category": "Koira", "multiplier": 5.0}, {"category": "Cat", "multiplier": -5.0}]']

        response = self.survey_service.delete_category_in_questions(
            question_ids,
            questions_weights
        )
        self.assertTrue(response)
        self.repo_mock.remove_category_from_question.assert_any_call(
            question_ids[0],
            questions_weights[0]
        )
        self.repo_mock.remove_category_from_question.assert_any_call(
            question_ids[1],
            questions_weights[1]
        )
        self.repo_mock.remove_category_from_question.assert_any_call(
            question_ids[2],
            questions_weights[2]
        )
        call_count = self.repo_mock.remove_category_from_question.call_count
        self.assertEqual(call_count, 3)

    def test_delete_category_results_for_category_calls_repo_correctly(self):
        self.repo_mock.delete_category_results_of_category.return_value = True
        result = self.survey_service.delete_category_results_for_category(1, 1)
        self.assertTrue(result)
        self.repo_mock.delete_category_results_of_category.assert_called_with(
            1)
