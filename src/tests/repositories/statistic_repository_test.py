from ast import excepthandler
import unittest
import uuid
from datetime import datetime, timedelta

from repositories.survey_repository import SurveyRepository
from repositories.statistic_repository import StatisticRepository

from app import create_app

class TestStatisticRepository(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.repo = SurveyRepository()
        self.srepo = StatisticRepository()

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

            group_id = self.srepo._add_user_group(survey_id)

            user_id_1 = self.srepo._add_user()
            user_id_2 = self.srepo._add_user()
            user_id_3 = self.srepo._add_user(group_id)

            self.srepo._add_user_answers(user_id_1, [answer_id_1, answer_id_4])
            self.srepo._add_user_answers(user_id_2, [answer_id_1, answer_id_3])
            self.srepo._add_user_answers(user_id_3, [answer_id_2, answer_id_4])

        return survey_id, group_id

    def test_number_of_submissions(self):
        with self.app.app_context():
            survey_id = self.repo.survey_exists("Elephants")[1]
            result = self.srepo.get_number_of_submissions(survey_id)

        self.assertEqual(result, 5)

    def test_answer_distribution(self):
        with self.app.app_context():
            survey_id = self.repo.survey_exists("Elephants")[1]
            result = self.srepo.get_answer_distribution(survey_id)

        self.assertEqual(result[0][4], 3)
        self.assertEqual(result[1][4], 2)

    def test_answer_distribution_filtered_by_email(self):
        with self.app.app_context():
            survey_id = self.repo.survey_exists("Elephants")[1]
            result = self.srepo.get_answer_distribution(
                survey_id, email="@")

        self.assertEqual(result[0][4], 3)
        self.assertEqual(result[1][4], 1)

    def test_answer_distribution_per_user_group(self):
        with self.app.app_context():
            survey_id = self.repo.survey_exists("Elephants")[1]
            group_id = self.srepo.find_user_group_by_name("Supertestaajat")
            result = self.srepo.get_answer_distribution(
                survey_id, user_group_id=group_id)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][4], 1)

    def test_answer_distribution_filtered_by_date(self):
        with self.app.app_context():
            start_date = datetime.fromisoformat("2022-10-01")
            end_date = datetime.fromisoformat("2022-11-02")
            survey_id = self.repo.survey_exists("Elephants")[1]
            result = self.srepo.get_answer_distribution(
                survey_id, start_date=start_date, end_date=end_date)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][2], 33)

    def test_answer_distribution_filtered_by_date_no_answers_in_range(self):
        with self.app.app_context():
            start_date = datetime.fromisoformat("2021-01-01")
            end_date = datetime.fromisoformat("2021-12-31")
            survey_id = self.repo.survey_exists("Elephants")[1]
            result = self.srepo.get_answer_distribution(
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
            survey_user_group_id = self.srepo._add_survey_user_group(
                survey_user_group_name, survey_id)
            question_id = self.repo.create_question(
                "What?",
                survey_id,
                '[{"category": "Boo", "multiplier": 1.0}]'
            )
            answer_id = self.repo.create_answer("No", 12, question_id)
            user_email = "jukka@haapalainen.com"
            user_id = self.srepo._add_user(user_email, survey_user_group_id)

            users_who_answered_survey_before = self.srepo.get_users_who_answered_survey(
                survey_id)
            self.srepo._add_user_answers(user_id, [answer_id])

            users_who_answered_survey_after = self.srepo.get_users_who_answered_survey(
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
            survey_user_group_id = self.srepo._add_survey_user_group(
                survey_user_group_name, survey_id_2)
            question_id = self.repo.create_question(
                "Que?",
                survey_id_2,
                '[{"category": "Oraleee", "multiplier": 1.0}]'
            )
            answer_id = self.repo.create_answer("No", 12, question_id)
            user_email = "peña@nieto.com"
            user_id = self.srepo._add_user(user_email, survey_user_group_id)

            self.srepo._add_user_answers(user_id, [answer_id])

            users_who_answered_survey = self.srepo.get_users_who_answered_survey(
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
            survey_user_group_id = self.srepo._add_survey_user_group(
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
            user_id_1 = self.srepo._add_user(user_email_1, survey_user_group_id)
            user_id_2 = self.srepo._add_user(user_email_2, survey_user_group_id)

            self.srepo._add_user_answers(user_id_1, [answer_id],  answer_date_1)
            self.srepo._add_user_answers(user_id_2, [answer_id])

            start_date = datetime.fromisoformat("2011-10-04 00:00:21.283")
            end_date = datetime.fromisoformat("2012-10-04 00:00:21.283")

            users_non_filtered = self.srepo.get_users_who_answered_survey(
                survey_id)
            users_filtered = self.srepo.get_users_who_answered_survey(
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
            survey_user_group_id_1 = self.srepo._add_survey_user_group(
                survey_user_group_name_1, survey_id)
            survey_user_group_id_2 = self.srepo._add_survey_user_group(
                survey_user_group_name_2, survey_id)
            question_id = self.repo.create_question(
                "Tomorrow?",
                survey_id,
                '[{"category": "Infinity", "multiplier": 1.0}]'
            )

            answer_id = self.repo.create_answer("Today", 10, question_id)
            user_email_1 = "email@gmail.com"
            user_email_2 = "korppi@norppa.fi"
            user_id_1 = self.srepo._add_user(
                user_email_1, survey_user_group_id_1)
            user_id_2 = self.srepo._add_user(
                user_email_2, survey_user_group_id_2)

            self.srepo._add_user_answers(user_id_1, [answer_id])
            self.srepo._add_user_answers(user_id_2, [answer_id])

            users_non_filtered = self.srepo.get_users_who_answered_survey(
                survey_id)
            users_filtered = self.srepo.get_users_who_answered_survey(
                survey_id, group_id=survey_user_group_id_1)

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
            user_group_1_id = self.srepo._add_survey_user_group(group_name=user_group_1_name,
                                                               survey_id=survey_id)
            user_group_2_name = "group2"
            user_group_2_id = self.srepo._add_survey_user_group(group_name=user_group_2_name,
                                                               survey_id=survey_id)

            advanced_user_id = self.srepo._add_user(
                email="Advanced", group_id=user_group_1_id)
            beginner_user_id = self.srepo._add_user(
                email="Beginner", group_id=user_group_2_id)

            self.srepo._add_user_answers(
                advanced_user_id, [answer_one_good_id,      answer_two_decent_id])
            self.srepo._add_user_answers(
                beginner_user_id, [answer_one_decent_id,    answer_two_bad_id])
            #  question | total points  | category weight   |  weighted points / answers
            #   1       |   7           | Math x 2          | 14 / 2 = 7
            #   2       |   -3          | Math x 1          | -3 / 2 = -1.5
            #   2       |   -3          | Statistics x2     | -6 / 2 = -3

            start_date_old = datetime.fromisoformat("2012-11-02")
            end_date_old = datetime.fromisoformat("2013-11-02")
            start_date_current = datetime.today() - timedelta(days=1)
            end_date_current = datetime.today() + timedelta(days=1)

            sum_for_question_one = self.srepo.get_sum_of_user_answer_points_by_question_id(
                question_one_id)
            sum_for_question_two = self.srepo.get_sum_of_user_answer_points_by_question_id(
                question_two_id)
            sum_for_question_one_filter_date_old = self.srepo.get_sum_of_user_answer_points_by_question_id(
                question_one_id, start_date=start_date_old, end_date=end_date_old)
            sum_for_question_one_filter_date_current = self.srepo.get_sum_of_user_answer_points_by_question_id(
                question_one_id, start_date=start_date_current, end_date=end_date_current)
            sum_for_question_one_filter_group_1 = self.srepo.get_sum_of_user_answer_points_by_question_id(
                question_one_id, user_group_id=user_group_1_id)
            sum_for_question_one_filter_group_2 = self.srepo.get_sum_of_user_answer_points_by_question_id(
                question_one_id, user_group_id=user_group_2_id)
            sum_for_question_two_filter_group_1 = self.srepo.get_sum_of_user_answer_points_by_question_id(
                question_two_id, user_group_id=user_group_1_id)
            sum_for_question_two_filter_group_2 = self.srepo.get_sum_of_user_answer_points_by_question_id(
                question_two_id, user_group_id=user_group_2_id)

            self.assertEquals(sum_for_question_one, 7)
            self.assertEquals(sum_for_question_two, -3)
            self.assertEquals(sum_for_question_one_filter_date_old, 0)
            self.assertEquals(sum_for_question_one_filter_date_current, 7)
            self.assertEquals(sum_for_question_one_filter_group_1, 5)
            self.assertEquals(sum_for_question_one_filter_group_2, 2)
            self.assertEquals(sum_for_question_two_filter_group_1, 2)
            self.assertEquals(sum_for_question_two_filter_group_2, -5)

            count_answers_for_question_one = self.srepo.get_count_of_user_answers_to_a_question(
                question_one_id)
            count_answers_for_question_two = self.srepo.get_count_of_user_answers_to_a_question(
                question_two_id)
            count_answers_for_question_one_filter_date_old = self.srepo.get_count_of_user_answers_to_a_question(
                question_one_id, start_date=start_date_old, end_date=end_date_old)
            count_answers_for_question_one_filter_date_current = self.srepo.get_count_of_user_answers_to_a_question(
                question_one_id, start_date=start_date_current, end_date=end_date_current)

            count_answers_for_question_one_filter_group_1 = self.srepo.get_count_of_user_answers_to_a_question(
                question_one_id, user_group_1_id)
            count_answers_for_question_one_filter_group_2 = self.srepo.get_count_of_user_answers_to_a_question(
                question_one_id, user_group_1_id)
            count_answers_for_question_two_filter_group_1 = self.srepo.get_count_of_user_answers_to_a_question(
                question_one_id, user_group_1_id)
            count_answers_for_question_two_filter_group_2 = self.srepo.get_count_of_user_answers_to_a_question(
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
            averages = self.srepo.calculate_average_scores_by_category(11)
            averages_filter_group_1 = self.srepo.calculate_average_scores_by_category(
                survey_id, user_group_1_id)
            averages_filter_date_old = self.srepo.calculate_average_scores_by_category(
                survey_id, start_date=start_date_old, end_date=end_date_old)
            averages_filter_date_current = self.srepo.calculate_average_scores_by_category(
                survey_id, start_date=start_date_current, end_date=end_date_current)

            # (Math categories weighted average scores sum) / (count of math categories ):  5.5 / 2 = 2.75
            self.assertEqual(averages[0], (category_math_id, 'Math', 2.75))

            # Stats categories weighted average scores sum -3, only one category = -3
            self.assertTrue(averages[1] == (
                category_stats_id, "Statistics", -3))

            # (Math categories weighted average scores sum) / (count of math categories ):  12 / 2 = 6
            self.assertTrue(averages_filter_group_1[0] == (
                category_math_id, 'Math', 6))

            # Stats categories weighted average scores sum 4, only one category = 4
            self.assertTrue(averages_filter_group_1[1] == (
                category_stats_id, "Statistics", 4))

            self.assertTrue(averages == averages_filter_date_current)

            self.assertTrue(averages_filter_date_old[0] == (
                category_math_id, 'Math', None))
            self.assertTrue(averages_filter_date_old[1] == (
                category_stats_id, 'Statistics', None))

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

            user_one_id = self.srepo._add_user("One")
            user_two_id = self.srepo._add_user("Two")
            user_three_id = self.srepo._add_user("Three")

            self.srepo._add_user_answers(user_one_id, [answer_one_good_id])
            self.srepo._add_user_answers(user_two_id, [answer_one_great_id])
            self.srepo._add_user_answers(user_three_id, [answer_one_great_id])

            self.assertTrue(
                self.srepo.get_count_of_user_answers_to_a_question(question_one_id) == 3)
            self.assertTrue(
                self.srepo.get_sum_of_user_answer_points_by_question_id(question_one_id) == 7)
            resulting_list = self.srepo.calculate_average_scores_by_category(
                survey_id)
            self.assertTrue(resulting_list[0] == (
                category_one_id, "One", 2.33))
            self.assertTrue(resulting_list[1] == (
                category_two_id, "Two",  4.67))
            self.assertTrue(resulting_list[2] == (
                category_three_id, "Three", 7.0))

    def test_get_all_surveys_returns_correct_submission_count(self):
        self._create_survey_and_add_user_answers()

        with self.app.app_context():
            response = self.repo.get_all_surveys()

        submissions_first_survey = response[0][3]
        self.assertEqual(submissions_first_survey, 0)
        submissions_elephant_survey = response[5][3]
        self.assertEqual(submissions_elephant_survey, 5)
