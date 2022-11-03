from ast import excepthandler
import unittest
import uuid

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
                "Elephants", "What kind of an elephant are you?", "The amazing elephant survey!")
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

            group_id =  self.repo._add_user_group(survey_id)

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

        self.assertEqual(result, 3)

    
    # def test_number_of_submissions_per_user_group(self):
    #     survey_id, group_id = self.test_survey_id, self.test_user_group_id
    #     group_id_1 = uuid.uuid4()
    #     group_id_2 = group_id
    #     with self.app.app_context():
    #         result_1 = self.repo.get_number_of_submissions(survey_id, group_id_1)
    #         result_2 = self.repo.get_number_of_submissions(survey_id, group_id_2)

    #     self.assertEqual(result_1, None)
    #     self.assertEqual(result_2, 1)

    def test_answer_distribution(self):
        with self.app.app_context():
            survey_id = self.repo.survey_exists("Elephants")[1]
            result = self.repo.get_answer_distribution(survey_id)

        self.assertEqual(result[0][4], 2)
        self.assertEqual(result[1][4], 1)

    def test_answer_distribution_per_user_group(self):
        with self.app.app_context():
            survey_id = self.repo.survey_exists("Elephants")[1]
            group_id = self.repo._find_user_group_by_name("Supertestaajat")
            result = self.repo.get_answer_distribution(survey_id, group_id)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][4], 1)

    def test_get_users_who_answered_survey_returns_user_that_answered(self):
        with self.app.app_context():
            survey_id = self.repo.create_survey(
                "Math",
                "A matchematical survey",
                "Test your math skills"
            )
            survey_user_group_name = "Management"
            survey_user_group_id = self.repo._add_survey_user_group(survey_user_group_name, survey_id)
            question_id = self.repo.create_question(
                "What?", 
                survey_id,
                '[{"category": "Boo", "multiplier": 1.0}]' 
            )
            answer_id = self.repo.create_answer("No", 12, question_id)
            user_email = "jukka@haapalainen.com"
            user_id = self.repo._add_user(user_email, survey_user_group_id)

            users_who_answered_survey_before = self.repo.get_users_who_answered_survey(survey_id)
            self.repo._add_user_answers(user_id, [answer_id])

            users_who_answered_survey_after = self.repo.get_users_who_answered_survey(survey_id)
            
        
        self.assertIsNone(users_who_answered_survey_before)
        self.assertEqual(len(users_who_answered_survey_after), 1)
        self.assertEqual(users_who_answered_survey_after[0].id, user_id)
        self.assertEqual(users_who_answered_survey_after[0].email, user_email)
        self.assertEqual(users_who_answered_survey_after[0].group_name, survey_user_group_name)
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
            survey_user_group_name = "Presidentes"
            survey_user_group_id = self.repo._add_survey_user_group(survey_user_group_name, survey_id_2)
            question_id = self.repo.create_question(
                "Que?", 
                survey_id_2,
                '[{"category": "Oraleee", "multiplier": 1.0}]' 
            )
            answer_id = self.repo.create_answer("No", 12, question_id)
            user_email = "peña@nieto.com"
            user_id = self.repo._add_user(user_email, survey_user_group_id)

            self.repo._add_user_answers(user_id, [answer_id])

            users_who_answered_survey = self.repo.get_users_who_answered_survey(survey_id_1)

        self.assertIsNone(users_who_answered_survey)