from ast import excepthandler
import unittest
import uuid
from datetime import datetime, timedelta

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
        self.assertFalse(response[0])

    def test_get_survey_with_valid_id_returns_survey(self):

        with self.app.app_context():
            response = self.repo.get_survey(1)

        self.assertIsNotNone(response)

    def test_get_survey_with_invalid_id_returns_false(self):

        with self.app.app_context():
            response = self.repo.get_survey(999999)

        self.assertFalse(response)

    def test_get_survey_id_from_question_id_returns_correct_value(self):
        with self.app.app_context():
            survey_id = self.repo.create_survey(
                "Algorithms", "Sorting algorithms", "Have fun with sorting!")
            question_id = self.repo.create_question(
                "In which situations can a bubble sorting algorithm be useful?", survey_id, category_weights)
            received_id = self.repo.get_survey_id_from_question_id(question_id)
        self.assertTrue(received_id == survey_id)

    def test_get_question_id_from_answer_id_returns_correct_value(self):
        with self.app.app_context():
            survey_id = self.repo.create_survey(
                "Data structures", "Storing information", "Have fun with storing!")
            question_id = self.repo.create_question(
                "What are the drawbacks of hashmaps?", survey_id, category_weights)
            answer_id = self.repo.create_answer(
                text="Slow lookup times when looking by key", points=-10, question_id=question_id)
            received_id = self.repo.get_question_id_from_answer_id(answer_id)
        self.assertTrue(received_id == question_id)

    def test_update_survey_updated_at_changes_updated_field(self):
        with self.app.app_context():
            before = self.repo.get_survey(1)[3]
            self.repo.update_survey_updated_at(1)
            after = self.repo.get_survey(1)[3]
        self.assertGreater(after, before)

    def test_delete_question_answer_updates_survey_updated_at(self):
        with self.app.app_context():
            question_id = self.repo.create_question(
                "What brings you comfort?", 1, category_weights)
            answer_id = self.repo.create_answer("Unit tests", question_id, 5)
            before = self.repo.get_survey(1)[3]
            self.repo.delete_answer_from_question(answer_id)
            after = self.repo.get_survey(1)[3]
        self.assertGreater(after, before)

    def test_delete_question_updates_survey_updated_at(self):
        with self.app.app_context():
            question_id = self.repo.create_question(
                "Has my existence made any difference in the end?", 1, category_weights)
            before = self.repo.get_survey(1)[3]
            self.repo.delete_question_from_survey(question_id)
            after = self.repo.get_survey(1)[3]
        self.assertGreater(after, before)

    def test_create_category_updates_survey_updated_at(self):
        content_links = '[{"url":"https://www.eficode.com/cases/hansen","type":"Case Study"},{"url":"https://www.eficode.com/cases/basware","type":"Case Study"}]'
        with self.app.app_context():
            before = self.repo.get_survey(1)[3]
            self.repo.create_category(
                "1",
                "name",
                "description",
                content_links)
            after = self.repo.get_survey(1)[3]
            print("After:", after)
        self.assertGreater(after, before)

    def update_category_updates_survey_updated_at(self):
        content_links = '[{"url":"https://www.eficode.com/cases/hansen","type":"Case Study"},{"url":"https://www.eficode.com/cases/basware","type":"Case Study"}]'
        with self.app.app_context():
            before = self.repo.get_survey(1)[3]
            self.repo.update_category(
                "1",
                "name",
                "improved description",
                content_links)
            after = self.repo.get_survey(1)[3]
        self.assertGreater(after, before)

    def delete_category_updates_survey_updated_at(self):
        content_links = '[{"url":"https://www.eficode.com/cases/hansen","type":"Case Study"},{"url":"https://www.eficode.com/cases/basware","type":"Case Study"}]'
        with self.app.app_context():
            category = self.repo.create_category(
                "1",
                "name",
                "description",
                content_links)
            before = self.repo.get_survey(1)[3]
            self.repo.delete_category(category)
            after = self.repo.get_survey(1)[3]
        self.assertGreater(after, before)

    def survey_updated_at_remains_unaltered_without_changes(self):
        with self.app.app_context():
            before = self.repo.get_survey(1)
            after = self.repo.get_survey(1)
        self.assertEqual(after, before)

    def test_get_all_surveys_with_correct_question_counts(self):

        with self.app.app_context():
            response = self.repo.get_all_surveys()

        first_survey_with_questions = response[0][2]
        self.assertEqual(first_survey_with_questions, 12)
        second_survey_without_questions = response[1][2]
        self.assertEqual(second_survey_without_questions, 0)
        third_survey_with_a_question = response[2][2]
        self.assertEqual(third_survey_with_a_question, 1)

    def test_get_all_surveys_returns_correct_amount_of_surveys(self):

        with self.app.app_context():
            response = self.repo.get_all_surveys()
        self.assertEqual(len(response), 7)

    def test_get_all_surveys_returns_correct_submission_count(self):
        self._create_survey_and_add_user_answers()

        with self.app.app_context():
            response = self.repo.get_all_surveys()

        submissions_first_survey = response[0][3]
        self.assertEqual(submissions_first_survey, 0)
        submissions_last_survey = response[7][3]
        self.assertEqual(submissions_last_survey, 3)

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
                question_id, new_text, category_weights, [], [])

            result_get_new = self.repo.get_question(question_id)

        self.assertTrue(result_update)
        self.assertEqual(result_get_new.text, "update question test")

    def test_update_question_updates_answers(self):

        with self.app.app_context():
            question_id = 10
            question = self.repo.get_question(question_id)
            original_answers = self.repo.get_question_answers(question_id)
            new_answers = [(original_answers[0][0], "changed", 2),
                           (original_answers[1][0], "muutettu", -2)]
            changed = self.repo.update_question(question_id, question[0], question[3],
                                                original_answers, new_answers)
            changed_answers = self.repo.get_question_answers(question_id)
            self.assertTrue(changed)
            self.assertEqual(new_answers, changed_answers)
            self.repo.update_question(question_id, question[0], question[3],
                                      changed_answers, original_answers)

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
            content_links = '[{"url":"https://www.eficode.com/cases/hansen","type":"Case Study"},{"url":"https://www.eficode.com/cases/basware","type":"Case Study"}]'
            response = self.repo.update_category(
                category_id,
                "name",
                "description",
                content_links)
        self.assertTrue(response != None)
        self.assertGreaterEqual(response, 0)

    def test_update_category_with_invalid_data_returns_False(self):
        with self.app.app_context():
            category_id = -1
            content_links = '[{"url":"https://www.eficode.com/cases/hansen","type":"Case Study"},{"url":"https://www.eficode.com/cases/basware","type":"Case Study"}]'
            response = self.repo.update_category(
                category_id,
                "name",
                "description",
                content_links)
        self.assertFalse(response)

        with self.app.app_context():
            category_id = 2.5
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

    def test_sucessful_update_category_returns_category(self):
        with self.app.app_context():
            content_links = '[{"url":"https://www.eficode.com/cases/hansen","type":"Case Study"},{"url":"https://www.eficode.com/cases/basware","type":"Case Study"}]'
            category_id = self.repo.create_category(
                "1",
                "name",
                "description",
                content_links)
            updated_category = self.repo.update_category(
                category_id,
                content_links,
                "A more descriptive name",
                "An actual description")
        self.assertTrue(updated_category != None)
        self.assertEquals(updated_category, category_id)

    def _create_survey_and_add_user_answers(self):
        """Creates a survey with user answers.
        Returns survey id, user group id"""
        with self.app.app_context():
            survey_id = self.repo.create_survey(
                "Elephants 2", "What kind of an elephant are you?", "The amazing elephant survey!")
            question_id_1 = self.repo.create_question(
                "Describe the size of your ears?", survey_id,
                '[{"category": "Size", "multiplier": 1.0}]')
            answer_id_1 = self.repo.create_answer("Huge", 5, question_id_1)
            answer_id_2 = self.repo.create_answer(
                "Nonexistent", 0, question_id_1)
            question_id_2 = self.repo.create_question(
                "Where do you prefer to hang out?", survey_id,
                '[{"category": "Habitat", "multiplier": 1.0}]')
            answer_id_3 = self.repo.create_answer("Forest", 5, question_id_2)
            answer_id_4 = self.repo.create_answer("Savannah", 0, question_id_2)

            group_id = self.repo._add_user_group(survey_id)

            user_id_1 = self.repo._add_user()
            user_id_2 = self.repo._add_user()
            user_id_3 = self.repo._add_user(group_id)

            self.repo._add_user_answers(user_id_1, [answer_id_1, answer_id_4])
            self.repo._add_user_answers(user_id_2, [answer_id_1, answer_id_3])
            self.repo._add_user_answers(user_id_3, [answer_id_2, answer_id_4])

        return survey_id, group_id

    def test_number_of_submissions(self):
        with self.app.app_context():
            survey_id = self.repo.survey_exists("Elephants")[1]
            result = self.repo.get_number_of_submissions(survey_id)

        self.assertEqual(result, 4)

    def test_answer_distribution(self):
        with self.app.app_context():
            survey_id = self.repo.survey_exists("Elephants")[1]
            result = self.repo.get_answer_distribution(survey_id)

        self.assertEqual(result[0][4], 3)
        self.assertEqual(result[1][4], 1)

    def test_answer_distribution_filtered(self):
        with self.app.app_context():
            survey_id = self.repo.survey_exists("Elephants")[1]
            result = self.repo.get_answer_distribution_filtered(survey_id,
                                                                None, None, '')

        self.assertEqual(result[0][4], 3)
        self.assertEqual(result[1][4], 1)

    def test_answer_distribution_per_user_group(self):
        with self.app.app_context():
            survey_id = self.repo.survey_exists("Elephants")[1]
            group_id = self.repo._find_user_group_by_name("Supertestaajat")
            result = self.repo.get_answer_distribution(
                survey_id, user_group_id=group_id)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][4], 1)

    def test_answer_distribution_filtered_by_date(self):
        with self.app.app_context():
            start_date = datetime.fromisoformat("2022-10-01")
            end_date = datetime.fromisoformat("2022-11-02")
            survey_id = self.repo.survey_exists("Elephants")[1]
            result = self.repo.get_answer_distribution(
                survey_id, start_date=start_date, end_date=end_date)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][2], 33)

    def test_answer_distribution_filtered_by_date_no_answers_in_range(self):
        with self.app.app_context():
            start_date = datetime.fromisoformat("2021-01-01")
            end_date = datetime.fromisoformat("2021-12-31")
            survey_id = self.repo.survey_exists("Elephants")[1]
            result = self.repo.get_answer_distribution(
                survey_id, start_date=start_date, end_date=end_date)

        self.assertFalse(result)

    def test_get_users_who_answered_survey_returns_user_that_answered(self):
        with self.app.app_context():
            survey_id = self.repo.create_survey(
                "Math",
                "A matchematical survey",
                "Test your math skills"
            )
            survey_user_group_name = "Management"
            survey_user_group_id = self.repo._add_survey_user_group(
                survey_user_group_name, survey_id)
            question_id = self.repo.create_question(
                "What?",
                survey_id,
                '[{"category": "Boo", "multiplier": 1.0}]'
            )
            answer_id = self.repo.create_answer("No", 12, question_id)
            user_email = "jukka@haapalainen.com"
            user_id = self.repo._add_user(user_email, survey_user_group_id)

            users_who_answered_survey_before = self.repo.get_users_who_answered_survey(
                survey_id)
            self.repo._add_user_answers(user_id, [answer_id])

            users_who_answered_survey_after = self.repo.get_users_who_answered_survey(
                survey_id)

        self.assertIsNone(users_who_answered_survey_before)
        self.assertEqual(len(users_who_answered_survey_after), 1)
        self.assertEqual(users_who_answered_survey_after[0].id, user_id)
        self.assertEqual(users_who_answered_survey_after[0].email, user_email)
        self.assertEqual(
            users_who_answered_survey_after[0].group_name, survey_user_group_name)
        self.assertIsNotNone(users_who_answered_survey_after[0].answer_time)

    def test_get_users_who_answered_survey_does_not_return_user_that_did_not_answer(self):
        with self.app.app_context():
            survey_id_1 = self.repo.create_survey(
                "French",
                "A french survey",
                "Test your oui skills"
            )
            survey_id_2 = self.repo.create_survey(
                "Spanish",
                "A spanish survey",
                "Test your olé skills"
            )
            self.repo.create_category(
                survey_id_2, "Oraleee", "Description", [])
            survey_user_group_name = "Presidentes"
            survey_user_group_id = self.repo._add_survey_user_group(
                survey_user_group_name, survey_id_2)
            question_id = self.repo.create_question(
                "Que?",
                survey_id_2,
                '[{"category": "Oraleee", "multiplier": 1.0}]'
            )
            answer_id = self.repo.create_answer("No", 12, question_id)
            user_email = "peña@nieto.com"
            user_id = self.repo._add_user(user_email, survey_user_group_id)

            self.repo._add_user_answers(user_id, [answer_id])

            users_who_answered_survey = self.repo.get_users_who_answered_survey(
                survey_id_1)

        self.assertIsNone(users_who_answered_survey)

    def test_get_users_who_answered_survey_when_given_datetime_returns_correct_users(self):
        with self.app.app_context():
            survey_id = self.repo.create_survey(
                "Time survey",
                "A survey about time",
                "When and where? And when?"
            )

            survey_user_group_name = "Presidentes"
            survey_user_group_id = self.repo._add_survey_user_group(
                survey_user_group_name, survey_id)

            question_id = self.repo.create_question(
                "Tomorrow?",
                survey_id,
                '[{"category": "Infinity", "multiplier": 1.0}]'
            )

            answer_id = self.repo.create_answer("Today", 10, question_id)
            user_email_1 = "email@gmail.com"
            user_email_2 = "korppi@norppa.fi"
            answer_date_1 = datetime.fromisoformat("2011-11-04 00:05:23.283")
            user_id_1 = self.repo._add_user(user_email_1, survey_user_group_id)
            user_id_2 = self.repo._add_user(user_email_2, survey_user_group_id)

            self.repo._add_user_answers(user_id_1, [answer_id],  answer_date_1)
            self.repo._add_user_answers(user_id_2, [answer_id])

            start_date = datetime.fromisoformat("2011-10-04 00:00:21.283")
            end_date = datetime.fromisoformat("2012-10-04 00:00:21.283")

            users_non_filtered = self.repo.get_users_who_answered_survey(
                survey_id)
            users_filtered = self.repo.get_users_who_answered_survey(
                survey_id, start_date, end_date)

        self.assertEqual(len(users_non_filtered), 2)
        self.assertEqual(len(users_filtered), 1)

    def test_get_users_who_answered_survey_belonging_to_given_group_returns_correct_users(self):
        with self.app.app_context():
            survey_id = self.repo.create_survey(
                "Time survey",
                "A survey about time",
                "When and where? And when?"
            )

            survey_user_group_name_1 = "Presidentes"
            survey_user_group_name_2 = "Peasants"
            survey_user_group_id_1 = self.repo._add_survey_user_group(
                survey_user_group_name_1, survey_id)
            survey_user_group_id_2 = self.repo._add_survey_user_group(
                survey_user_group_name_2, survey_id)
            question_id = self.repo.create_question(
                "Tomorrow?",
                survey_id,
                '[{"category": "Infinity", "multiplier": 1.0}]'
            )

            answer_id = self.repo.create_answer("Today", 10, question_id)
            user_email_1 = "email@gmail.com"
            user_email_2 = "korppi@norppa.fi"
            user_id_1 = self.repo._add_user(
                user_email_1, survey_user_group_id_1)
            user_id_2 = self.repo._add_user(
                user_email_2, survey_user_group_id_2)

            self.repo._add_user_answers(user_id_1, [answer_id])
            self.repo._add_user_answers(user_id_2, [answer_id])

            users_non_filtered = self.repo.get_users_who_answered_survey(
                survey_id)
            users_filtered = self.repo.get_users_who_answered_survey(
                survey_id, group_name="Presidentes")

        self.assertEqual(len(users_non_filtered), 2)
        self.assertEqual(len(users_filtered), 1)

    def test_get_user_answer_sum_of_points_and_count_answers(self):
        with self.app.app_context():
            survey_id = self.repo.create_survey(
                "Math survey", "Data Science and Math", "Are your data science skills above average or do you hit the mean?")
            question_one_id = self.repo.create_question(
                "How is the average calculated", survey_id,
                '[{"category": "Math", "multiplier": 2.0}]')
            question_two_id = self.repo.create_question(
                "What is the difference between the mean and the median?", survey_id,
                '[{"category": "Math", "multiplier": 1.0}, {"category": "Statistics", "multiplier": 2.0}]')
            question_with_no_answers_id = self.repo.create_question(
                "Are there any graphs on n vertices whose representation requires more than floor(n/2) copies of each letter?", survey_id,
                '[{"category": "Math", "multiplier": 5.0}]')
            category_math_id = self.repo.create_category(
                survey_id, "Math", "I'm the operator of my pocket calculator", '[]')
            category_stats_id = self.repo.create_category(
                survey_id, "Statistics", "Don't end up as a statistic.", '[]')

            answer_one_good_id = self.repo.create_answer(
                "Calculate sum of elements and divide by their number", 5, question_one_id)
            answer_one_decent_id = self.repo.create_answer(
                "Add stuff and divide", 2, question_one_id)

            answer_two_decent_id = self.repo.create_answer(
                "It has to do with the ways to calculate averages", 2, question_two_id)
            answer_two_bad_id = self.repo.create_answer(
                "The former is not nice.", -5, question_two_id)

            user_group_1_name = "group1"
            user_group_1_id = self.repo._add_survey_user_group(group_name=user_group_1_name,
                                                               survey_id=survey_id)
            user_group_2_name = "group2"            
            user_group_2_id = self.repo._add_survey_user_group(group_name=user_group_2_name,
                                                               survey_id=survey_id)

            advanced_user_id = self.repo._add_user(
                email="Advanced", group_id=user_group_1_id)
            beginner_user_id = self.repo._add_user(
                email="Beginner", group_id=user_group_2_id)

            self.repo._add_user_answers(
                advanced_user_id, [answer_one_good_id,      answer_two_decent_id])
            self.repo._add_user_answers(
                beginner_user_id, [answer_one_decent_id,    answer_two_bad_id])
            #  question | total points  | category weight   |  weighted points / answers
            #   1       |   7           | Math x 2          | 14 / 2 = 7
            #   2       |   -3          | Math x 1          | -3 / 2 = -1.5
            #   2       |   -3          | Statistics x2     | -6 / 2 = -3

            start_date_old = datetime.fromisoformat("2012-11-02")
            end_date_old = datetime.fromisoformat("2013-11-02")
            start_date_current = datetime.today() - timedelta(days=1)
            end_date_current = datetime.today() + timedelta(days=1)

            sum_for_question_one = self.repo.get_sum_of_user_answer_points_by_question_id(
                question_one_id)
            sum_for_question_two = self.repo.get_sum_of_user_answer_points_by_question_id(
                question_two_id)
            sum_for_question_one_filter_date_old = self.repo.get_sum_of_user_answer_points_by_question_id(
                question_one_id, start_date=start_date_old, end_date=end_date_old)
            sum_for_question_one_filter_date_current = self.repo.get_sum_of_user_answer_points_by_question_id(
                question_one_id, start_date=start_date_current, end_date=end_date_current)
            sum_for_question_one_filter_group_1 = self.repo.get_sum_of_user_answer_points_by_question_id(
                question_one_id, user_group_id=user_group_1_id)
            sum_for_question_one_filter_group_2 = self.repo.get_sum_of_user_answer_points_by_question_id(
                question_one_id, user_group_id=user_group_2_id)
            sum_for_question_two_filter_group_1 = self.repo.get_sum_of_user_answer_points_by_question_id(
                question_two_id, user_group_id=user_group_1_id)
            sum_for_question_two_filter_group_2 = self.repo.get_sum_of_user_answer_points_by_question_id(
                question_two_id, user_group_id=user_group_2_id)

            self.assertEquals(sum_for_question_one, 7)
            self.assertEquals(sum_for_question_two, -3)
            self.assertEquals(sum_for_question_one_filter_date_old, 0)
            self.assertEquals(sum_for_question_one_filter_date_current, 7)
            self.assertEquals(sum_for_question_one_filter_group_1, 5)
            self.assertEquals(sum_for_question_one_filter_group_2, 2)
            self.assertEquals(sum_for_question_two_filter_group_1, 2)
            self.assertEquals(sum_for_question_two_filter_group_2, -5)

            count_answers_for_question_one = self.repo.get_count_of_user_answers_to_a_question(
                question_one_id)
            count_answers_for_question_two = self.repo.get_count_of_user_answers_to_a_question(
                question_two_id)
            count_answers_for_question_one_filter_date_old = self.repo.get_count_of_user_answers_to_a_question(
                question_one_id, start_date=start_date_old, end_date=end_date_old)
            count_answers_for_question_one_filter_date_current = self.repo.get_count_of_user_answers_to_a_question(
                question_one_id, start_date=start_date_current, end_date=end_date_current)
            count_answers_for_question_three = self.repo.get_count_of_user_answers_to_a_question(
                question_with_no_answers_id)
            count_answers_for_question_one_filter_group_1 = self.repo.get_count_of_user_answers_to_a_question(
                question_one_id, user_group_1_id)
            count_answers_for_question_one_filter_group_2 = self.repo.get_count_of_user_answers_to_a_question(
                question_one_id, user_group_1_id)
            count_answers_for_question_two_filter_group_1 = self.repo.get_count_of_user_answers_to_a_question(
                question_one_id, user_group_1_id)
            count_answers_for_question_two_filter_group_2 = self.repo.get_count_of_user_answers_to_a_question(
                question_one_id, user_group_1_id)

            self.assertEquals(count_answers_for_question_one, 2)
            self.assertEquals(count_answers_for_question_two, 2)
            self.assertEquals(
                count_answers_for_question_one_filter_date_old, 0)
            self.assertEquals(
                count_answers_for_question_one_filter_date_current, 2)
            self.assertEquals(count_answers_for_question_one_filter_group_1, 1)
            self.assertEquals(count_answers_for_question_one_filter_group_2, 1)
            self.assertEquals(count_answers_for_question_two_filter_group_1, 1)
            self.assertEquals(count_answers_for_question_two_filter_group_2, 1)
            self.assertEquals(count_answers_for_question_three, 0)

            averages = self.repo.calculate_average_scores_by_category(
                survey_id)
            averages_filter_group_1 = self.repo.calculate_average_scores_by_category(
                survey_id, user_group_1_name)
            averages_filter_date_old = self.repo.calculate_average_scores_by_category(
                survey_id, start_date=start_date_old, end_date=end_date_old)
            averages_filter_date_current = self.repo.calculate_average_scores_by_category(
                survey_id, start_date=start_date_current, end_date=end_date_current)

            # (Math categories weighted average scores sum) / (count of math categories ):  5.5 / 3 = 1.83
            self.assertTrue(averages[0] == (category_math_id, 'Math', 1.83))
            # Stats categories weighted average scores sum -3, only one category = -3
            self.assertTrue(averages[1] == (
                category_stats_id, "Statistics", -3))

            # (Math categories weighted average scores sum) / (count of math categories ):  12 / 3 = 4
            self.assertTrue(averages_filter_group_1[0] == (
                category_math_id, 'Math', 4))
            # Stats categories weighted average scores sum 4, only one category = 4
            self.assertTrue(averages_filter_group_1[1] == (
                category_stats_id, "Statistics", 4))

            self.assertTrue(averages == averages_filter_date_current)
            self.assertTrue(averages_filter_date_old[0] == (
                category_math_id, 'Math', 0))
            self.assertTrue(averages_filter_date_old[1] == (
                category_stats_id, 'Statistics', 0))

    def test_get_user_answer_sum_of_points_and_count_answers_two(self):

        with self.app.app_context():
            survey_id = self.repo.create_survey(
                "Three category survey", "text", "More robust test coverage.")
            category_one_id = self.repo.create_category(
                survey_id, "One", "Description 1", '[]')
            category_two_id = self.repo.create_category(
                survey_id, "Two", "Description 2", '[]')
            category_three_id = self.repo.create_category(
                survey_id, "Three", "Description 3", '[]')

            question_one_id = self.repo.create_question(
                "Question one", survey_id, '[{"category": "One", "multiplier": 1.0}, {"category": "Two", "multiplier": 2.0}, {"category": "Three", "multiplier": 3.0}]')

            answer_one_good_id = self.repo.create_answer(
                "Returns 1 point", 1, question_one_id)
            answer_one_great_id = self.repo.create_answer(
                "Returns 3 points", 3, question_one_id)

            user_one_id = self.repo._add_user("One")
            user_two_id = self.repo._add_user("Two")
            user_three_id = self.repo._add_user("Three")

            self.repo._add_user_answers(user_one_id, [answer_one_good_id])
            self.repo._add_user_answers(user_two_id, [answer_one_great_id])
            self.repo._add_user_answers(user_three_id, [answer_one_great_id])

            self.assertTrue(
                self.repo.get_count_of_user_answers_to_a_question(question_one_id) == 3)
            self.assertTrue(
                self.repo.get_sum_of_user_answer_points_by_question_id(question_one_id) == 7)
            resulting_list = self.repo.calculate_average_scores_by_category(
                survey_id)
            self.assertTrue(resulting_list[0] == (
                category_one_id, "One", 2.33))
            self.assertTrue(resulting_list[1] == (
                category_two_id, "Two",  4.67))
            self.assertTrue(resulting_list[2] == (
                category_three_id, "Three", 7.0))

    def test_create_category_result(self):
        with self.app.app_context():
            category_id = self.repo.create_category(
                1, "cat", "cat is for category", [])
            text = "Category result text"
            cutoff_from_maxpts = 1.0
            category_result_id = self.repo.create_category_result(
                category_id,
                text,
                cutoff_from_maxpts)
            related_category_results = self.repo.get_category_results_from_category_id(category_id)[
                0]
            print(related_category_results, " - ", related_category_results[0])
            self.assertEquals(related_category_results[0], category_result_id)
            self.assertEquals(related_category_results[1], category_id)
            self.assertEquals(
                related_category_results[2], "Category result text")
            self.assertEquals(related_category_results[3], 1.0)

    def test_category_can_contain_multiple_category_results(self):
        with self.app.app_context():
            category_id = self.repo.create_category(
                1, "cat", "cat is for category", [])
            text = "Category result text 1"
            cutoff_from_maxpts = 1.0
            self.repo.create_category_result(
                category_id,
                text,
                cutoff_from_maxpts
            )

            text = "Category result text 2"
            cutoff_from_maxpts = 0.7
            self.repo.create_category_result(
                category_id,
                text,
                cutoff_from_maxpts
            )

            related_category_results = self.repo.get_category_results_from_category_id(
                category_id)
            self.assertTrue(len(related_category_results) == 2)

    def test_category_result_is_not_created_if_cutoff_exists(self):
        with self.app.app_context():
            category_id = self.repo.create_category(
                1, "cat", "cat is for category", [])
            text = "Category result text 1"
            cutoff_from_maxpts = 1.0
            self.repo.create_category_result(
                category_id,
                text,
                cutoff_from_maxpts
            )

            text = "Category result text 2"
            duplicate_cutoff = 1.0
            result = self.repo.create_category_result(
                category_id,
                text,
                duplicate_cutoff
            )
            self.assertIsNone(result)

    def test_create_a_survey_result_with_unique_cutoff_value(self):
        with self.app.app_context():
            result_id = self.repo.create_survey_result(
                8, "You seem to be an African elephant", 1.0)
        self.assertTrue(result_id)

    def test_survey_result_needs_to_have_unique_cutoff_value(self):
        with self.app.app_context():
            result_id = self.repo.create_survey_result(
                8, "You look like an Indian elephant", 1.0)
        self.assertFalse(result_id)

    def test_get_survey_results_returns_correct_amount_of_results(self):
        with self.app.app_context():
            self.repo.create_survey_result(
                8, "You look like an Indian elephant", 0.5)
            results = self.repo.get_survey_results(8)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[1][1], "You seem to be an African elephant")
        self.assertEqual(results[0][1], "You look like an Indian elephant")

    def test_delete_survey_result_deletes_survey_result(self):
        with self.app.app_context():
            self.repo.create_survey_result(
                8, "You look like an Indian elephant", 0.5)
            results = self.repo.get_survey_results(8)
            self.assertEqual(len(results), 2)

            response = self.repo.delete_survey_result(results[0][0])
            self.assertTrue(response)
            results = self.repo.get_survey_results(8)
            self.assertEqual(len(results), 1)

    def test_update_survey_results_updates_results_correctly(self):
        with self.app.app_context():
            survey_id = self.repo.create_survey("Goodness","How good are you",
            "Are you good? Or perhaps just decent?")
            original_results = [["Bad",0.3],["Good",0.6],["Great",1.0]]
            new_results = [["Decent",0.4],["Great",0.7],["Fantastic",1.0]]
            result_ids = []
            for result in original_results:
                result_ids.append(self.repo.create_survey_result(
                    survey_id, result[0], result[1]))
            or2 = []
            nr2 = []
            for i in range(3):
                or2.append((result_ids[i],original_results[i][0],original_results[i][1]))
                nr2.append((result_ids[i],new_results[i][0],new_results[i][1]))
            self.repo.update_survey_results(or2,nr2,survey_id)
            results = self.repo.get_survey_results(survey_id)
            self.assertEqual(results, nr2)
