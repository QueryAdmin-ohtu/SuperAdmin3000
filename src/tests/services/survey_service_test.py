import unittest
from datetime import datetime
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
            question_id, text, category_weights, [], [])
        self.assertEqual(check, 1)
        self.repo_mock.update_question.assert_called_with(
            question_id, text, category_weights, [], [])

    def test_create_category_calls_repo_correctly(self):
        self.repo_mock.create_category.return_value = 1
        survey_id = "1"
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

    def test_get_users_who_answered_survey(self):
        repo_return_value = [1, "jorma@uotinen.com", "This is a group"]
        self.repo_mock.get_users_who_answered_survey.return_value = repo_return_value
        survey_id = 1

        returned_value = self.survey_service.get_users_who_answered_survey(
            survey_id)
        self.repo_mock.get_users_who_answered_survey.assert_called_with(
            survey_id)
        self.assertEqual(returned_value, repo_return_value)

    def test_get_number_of_submissions_for_survey_calls_repo_correctly(self):
        self.repo_mock.get_number_of_submissions.return_value = 2
        survey_id = 1
        self.survey_service.get_number_of_submissions_for_survey(survey_id)
        self.repo_mock.get_number_of_submissions.assert_called_with(
            survey_id
        )

    def test_get_answer_distribution_for_survey_questions_calls_repo_correctly(self):
        self.repo_mock.get_answer_distribution.return_value = "None"
        survey_id = 1
        self.survey_service.get_answer_distribution_for_survey_questions(
            survey_id)
        self.repo_mock.get_answer_distribution_filtered.assert_called_with(
            survey_id, None, None, '', '')

    def test_get_users_who_answered_survey_in_timerange_returns_none_with_invalid_timerage(self):
        start_date_1 = datetime.fromisoformat("2011-11-04 00:05:23.283")
        end_date_1 = datetime.fromisoformat("2010-11-04 00:05:23.283")
        start_date_2 = datetime.fromisoformat("2015-11-04 00:05:23.283")
        end_date_2 = datetime.fromisoformat("2014-11-04 00:05:23.283")

        service_response_1 = self.survey_service.get_users_who_answered_survey_in_timerange(
            1, start_date_1, end_date_1)
        service_response_2 = self.survey_service.get_users_who_answered_survey_in_timerange(
            1, start_date_2, end_date_2)
        self.assertIsNone(service_response_1)
        self.assertIsNone(service_response_2)
        self.repo_mock.get_users_who_answered_survey.assert_not_called()

    def test_get_users_who_answered_survey_in_timerange_calls_repo_correctly_with_valid_timerange(self):
        survey_id = 1
        start_date = datetime.fromisoformat("2020-11-04 00:05:23.283")
        end_date = datetime.fromisoformat("2021-11-04 00:05:23.283")
        repo_value_to_return = [5, "timppa@gmail.com",
                                "Boss Team", "2021-10-04 00:05:23.283"]

        self.repo_mock.get_users_who_answered_survey.return_value = repo_value_to_return

        survey_reponse = self.survey_service.get_users_who_answered_survey_in_timerange(
            survey_id, start_date, end_date)

        self.repo_mock.get_users_who_answered_survey.assert_called_once_with(
            survey_id, start_date, end_date)
        self.assertEqual(repo_value_to_return, survey_reponse)

    def test_get_users_who_answered_survey_in_group_calls_repo_correctly_with_valid_group(self):
        survey_id = 1
        repo_value_to_return = [5, "timppa@gmail.com",
                                "Boss Team", "2021-10-04 00:05:23.283"]
        self.repo_mock.get_users_who_answered_survey.return_value = repo_value_to_return

        survey_reponse = self.survey_service.get_users_who_answered_survey_in_group(
            survey_id, group_name="Boss Team")

        self.repo_mock.get_users_who_answered_survey.assert_called_once_with(
            survey_id, group_name="Boss Team")
        self.assertEqual(repo_value_to_return, survey_reponse)

    def test_get_users_who_answered_survey_filtered_calls_repo_correctly_with_valid_arguments(self):
        survey_id = 1
        start_date = datetime.fromisoformat("2020-11-04 00:05:23.283")
        end_date = datetime.fromisoformat("2021-11-04 00:05:23.283")

        repo_value_to_return = [5, "timppa@gmail.com",
                                "Boss Team", "2021-10-04 00:05:23.283"]
        self.repo_mock.get_users_who_answered_survey.return_value = repo_value_to_return

        survey_reponse = self.survey_service.get_users_who_answered_survey_filtered(
            survey_id, start_date, end_date, "Boss Team", "boss@mail")

        self.repo_mock.get_users_who_answered_survey.assert_called_once_with(
            survey_id, start_date, end_date, "Boss Team", "boss@mail")
        self.assertEqual(repo_value_to_return, survey_reponse)

    def test_get_users_who_answered_survey_filtered_returns_none_with_invalid_timerage(self):
        start_date_1 = datetime.fromisoformat("2011-11-04 00:05:23.283")
        end_date_1 = datetime.fromisoformat("2010-11-04 00:05:23.283")

        service_response_1 = self.survey_service.get_users_who_answered_survey_filtered(
            1, start_date_1, end_date_1, "group", "mail")
        self.assertIsNone(service_response_1)

        self.repo_mock.get_users_who_answered_survey.assert_not_called()

    def test_get_users_who_answered_survey_filtered_works_with_empty_string_as_group(self):
        survey_id = 1
        start_date = datetime.fromisoformat("2020-11-04 00:05:23.283")
        end_date = datetime.fromisoformat("2021-11-04 00:05:23.283")

        repo_value_to_return = [5, "timppa@gmail.com",
                                "", "2021-10-04 00:05:23.283"]
        self.repo_mock.get_users_who_answered_survey.return_value = repo_value_to_return

        survey_reponse = self.survey_service.get_users_who_answered_survey_filtered(
            survey_id, start_date, end_date, "", "")

        self.repo_mock.get_users_who_answered_survey.assert_called_once_with(
            survey_id, start_date, end_date, None, "")
        self.assertEqual(repo_value_to_return, survey_reponse)

    def test_calculate_average_scores_by_category_calls_repo_correctly(self):
        value_to_return = [(1, "Category 1", 1.0)]
        self.repo_mock.calculate_average_scores_by_category.return_value = value_to_return
        survey_id = 1
        self.survey_service.calculate_average_scores_by_category(survey_id)
        self.repo_mock.calculate_average_scores_by_category.assert_called_with(
            survey_id,
            None,
            None,
            None
        )

    def test_calculate_average_scores_by_category_does_not_call_repo_with_invalid(self):
        survey_id = 1
        start_date = datetime.fromisoformat("2020-11-04 00:05:23.283")
        end_date = datetime.fromisoformat("2019-11-04 00:05:23.283")

        return_value = self.survey_service.calculate_average_scores_by_category(
            survey_id, start_date=start_date, end_date=end_date)
        self.repo_mock.calculate_average_scores_by_category.assert_not_called()
        self.assertIsNone(return_value)

    def test_calculate_average_scores_by_category_calls_repo_correctly_when_filtering(self):
        start_date = datetime.fromisoformat("2020-11-04 00:05:23.283")
        end_date = datetime.fromisoformat("2021-11-04 00:05:23.283")
        user_group_id = 22
        user_group_name = "Group 1"
        survey_id = 1
        repo_value_to_return = [(1, "Category 1", 1.0)]
        service_value_to_return = [(1, "Category 1", 1.0, 1.0)]
        self.repo_mock.calculate_average_scores_by_category.return_value = repo_value_to_return
        returned_value = self.survey_service.calculate_average_scores_by_category(
            survey_id,
            user_group_name,
            start_date,
            end_date
        )
        self.repo_mock.calculate_average_scores_by_category.assert_called_with(
            survey_id,
            user_group_name,
            start_date,
            end_date
        )
        self.assertEqual(service_value_to_return, returned_value)

    def test_create_category_result_calls_repo_correctly(self):
        self.repo_mock.create_category_result.return_value = 1
        category_id = 1
        text = "Dynamically fetched category result text"
        cutoff_from_maxpts = 1.0
        response = self.survey_service.create_category_result(
            category_id,
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
        original_results = [[5,"Bad",0.3],[6,"Good",1.0]]
        new_results = [[5,"Decent",0.3],[6,"Great",1.0]]
        response = self.survey_service.update_survey_results(original_results,
        new_results,3)
        self.assertTrue(response)
        self.repo_mock.update_survey_results.assert_called_with(original_results,
        new_results,3)
