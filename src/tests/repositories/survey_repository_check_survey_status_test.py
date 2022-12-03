from ast import excepthandler
import unittest
import uuid
from datetime import datetime, timedelta

from repositories.survey_repository import SurveyRepository

from app import create_app

class TestSurveyRepository(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.repo = SurveyRepository()

    def createSurvey(self, title):
        survey_id = self.repo.create_survey("Survey Status Should Be Ok!", title, "This will return a list")
        return survey_id

    def deleteSurvey(self, survey_id):
        self.repo.delete_survey(survey_id)

    
    category_weights = '[{"category": "status category 1", "multiplier": 10.0}, {"category": "status category 2", "multiplier": 20.0}]'
    index_of_survey_without_results = 9 # Hardcoded into schema.sql

    def test_check_survey_status_where_no_survey_results_returns_correct(self):
        with self.app.app_context():
            survey_id = self.repo.get_survey(self.index_of_survey_without_results)[0]
            check = self.repo.check_survey_status(survey_id)
            self.assertTrue(check[1])
            check = self.repo.check_survey_status(1)
            self.assertFalse(check[1])

    def test_check_survey_status_where_no_categories_returns_correct(self):
        with self.app.app_context():
            survey_id = self.repo.get_survey(self.index_of_survey_without_results)[0]
            check = self.repo.check_survey_status(survey_id)
            self.assertTrue(check[2])
            check = self.repo.check_survey_status(1)
            self.assertFalse(check[2])

    def test_check_survey_status_where_no_categories_without_category_results_returns_correct(self):
        with self.app.app_context():
            survey_id = self.repo.get_survey(self.index_of_survey_without_results)[0]
            check = self.repo.check_survey_status(survey_id)
            self.assertEquals(check[3], [])

    def test_check_survey_status_where_categories_without_category_results_exist_returns_correct(self):
        with self.app.app_context():
            check = self.repo.check_survey_status(8)
            self.assertEquals(check[3], ['Size', 'Habitat'])

    def test_check_survey_status_where_no_questions_returns_correct(self):
        with self.app.app_context():
            survey_id = self.repo.get_survey(self.index_of_survey_without_results)[0]
            check = self.repo.check_survey_status(survey_id)
            self.assertTrue(check[4])
            check = self.repo.check_survey_status(1)
            self.assertFalse(check[4])

    def test_check_survey_status_where_no_question_answers_returns_correct(self):
        with self.app.app_context():
            survey_id = self.createSurvey("no_question_answers")
            self.repo.create_question("mock question one", survey_id, self.category_weights)

            check = self.repo.check_survey_status(survey_id)
            self.assertEqual(check[5], ["mock question one"])
            
            question_two_id = self.repo.create_question("mock question two", survey_id, self.category_weights)
            check = self.repo.check_survey_status(survey_id)
            self.assertEqual(check[5], ["mock question one", "mock question two"])

            self.repo.create_answer("mock answer to question two", 0, question_two_id)
            check = self.repo.check_survey_status(survey_id)
            self.assertEqual(check[5], ["mock question one"])

            self.deleteSurvey(survey_id)
    
    def test_check_survey_status_where_one_question_without_categories_returns_correct(self):
        with self.app.app_context():
            survey_id = self.createSurvey("question_without_categories")
            self.repo.create_question("mock question one",survey_id, '[{"category": "status category 1", "multiplier": 0.0}, {"category": "status category 2", "multiplier": 0.0}]' )
            check = self.repo.check_survey_status(survey_id)
            self.assertTrue(check[6] == ["mock question one"])
            self.deleteSurvey(survey_id)

    def test_check_survey_status_where_multiple_question_without_categories_returns_correct(self):
        with self.app.app_context():
            survey_id = self.createSurvey("questions_without_categories")
            self.repo.create_question("mock question one",survey_id, '[{"category": "status category 1", "multiplier": 0.0}, {"category": "status category 2", "multiplier": 0.0}]' )
            check = self.repo.check_survey_status(survey_id)
            self.assertTrue(check[6] == ["mock question one"])
            self.repo.create_question("mock question two", survey_id, '[{"category": "status category 1", "multiplier": 0.0}, {"category": "status category 2", "multiplier": 0.0}]')
            check = self.repo.check_survey_status(survey_id)
            self.assertTrue(check[6] == ["mock question one", "mock question two"])
            self.deleteSurvey(survey_id)

    def test_check_survey_status_where_mix_of_questions_without_categories_returns_correct(self):
        with self.app.app_context():
            survey_id = self.createSurvey("questions_without_categories")
            self.repo.create_question("mock question one",survey_id, '[{"category": "status category 1", "multiplier": 0.0}, {"category": "status category 2", "multiplier": 0.1}]' )
            self.repo.create_question("mock question two", survey_id, '[{"category": "status category 1", "multiplier": 0.0}, {"category": "status category 2", "multiplier": 0.0}]')
            self.repo.create_question("mock question three", survey_id, '[{"category": "status category 1", "multiplier": 1.0}, {"category": "status category 2", "multiplier": 0.0}]')
            check = self.repo.check_survey_status(survey_id)
            self.assertTrue(check[6] == ["mock question two"])
            self.deleteSurvey(survey_id)

    def test_check_survey_status_where_categories_without_questions_returns_correct(self):
        with self.app.app_context():
            survey_id = self.createSurvey("categories_without_questions")
            self.deleteSurvey(survey_id)

    def test_check_survey_status_where_no_problems_present_returns_correct(self):
            with self.app.app_context():
                survey_id = self.createSurvey("no_problems_present")
                category_id = self.repo.create_category(survey_id, "status category 1", "Mock Description", [])
                self.repo.create_survey_result(survey_id, "Magnificient!", 1.0)
                self.repo.create_category_result(category_id, "Magnificient!", 1.0)
                question_id = self.repo.create_question("Question with answers and so forth!", survey_id, '[{"category": "status category 1", "multiplier": 1.0}]')
                self.repo.create_answer("Answer to question", 1, question_id)
                check = self.repo.check_survey_status(survey_id)
                self.assertEquals(len(check), 9)
                self.assertEquals(check, ['green', False, False, [], False, [], [], [], {}])
                self.deleteSurvey(survey_id)

    def test_check_survey_status_returns_red(self):
        with self.app.app_context():
                survey_id = self.createSurvey("Red Problems")
                self.assertEquals(self.repo.check_survey_status(survey_id)[0], "red")
                category_id = self.repo.create_category(survey_id, "status category 1", "Mock Description", [])
                self.assertEquals(self.repo.check_survey_status(survey_id)[0], "red")
                self.repo.create_survey_result(survey_id, "Magnificient!", 1.0)
                self.assertEquals(self.repo.check_survey_status(survey_id)[0], "red")
                self.repo.create_category_result(category_id, "Magnificient!", 1.0)
                self.assertEquals(self.repo.check_survey_status(survey_id)[0], "red")
                question_id = self.repo.create_question("Question with answers and so forth!", survey_id, '[{"category": "status category 1", "multiplier": 1.0}]')
                self.assertEquals(self.repo.check_survey_status(survey_id)[0], "red")
                self.repo.create_answer("Answer to question", 1, question_id)
                self.assertEquals(self.repo.check_survey_status(survey_id)[0], "green")
                self.deleteSurvey(survey_id)

    def test_check_survey_status_returns_yellow(self):
        with self.app.app_context():
                survey_id = self.createSurvey("Yellow Problems")
                category_id = self.repo.create_category(survey_id, "status category 1", "Mock Description", [])
                category_id_no_questions = self.repo.create_category(survey_id, "No questions", "Leads to yellow status", [])
                self.repo.create_survey_result(survey_id, "Magnificient!", 1.0)
                self.repo.create_category_result(category_id, "Magnificient!", 1.0)
                self.repo.create_category_result(category_id_no_questions, "Magnificient!", 1.0)
                question_id = self.repo.create_question("Question with answers and so forth!", survey_id, '[{"category": "status category 1", "multiplier": 0.0}]')
                self.repo.create_answer("Answer to question", 1, question_id)

                self.assertEquals(self.repo.check_survey_status(survey_id)[0], "yellow")
                self.deleteSurvey(survey_id)

    def test_get_unrelated_categories_in_weights_returns_unrelated_category_names(self):
        questions = [(1, 'Q1', 10, [{'category': 'catA', 'multiplier': 1.0}], 2022, 2022),
                     (2, 'Q2', 10, [{'category': 'missing', 'multiplier': 1.0}], 2022, 2022)]
        categories = [(101, 'catA', 'description', 10, [], 2022, 2022)]

        result = self.repo.get_unrelated_categories_in_weights(categories, questions)

        self.assertEqual(result, {'Q2': ['missing']})
