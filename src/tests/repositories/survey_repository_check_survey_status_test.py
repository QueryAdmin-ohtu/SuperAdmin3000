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

    def test_check_survey_status_when_no_survey_results_returns_correct(self):
        with self.app.app_context():
            survey_id = self.repo.get_survey(self.index_of_survey_without_results)
            check = self.repo.check_survey_status(survey_id)
            self.assertTrue(check[1] == True)
            check = self.repo.check_survey_status(1)
            self.assertTrue(check[1] == False)

    def test_check_survey_status_when_no_category_results_returns_correct(self):
        with self.app.app_context():
            survey_id = self.repo.get_survey(self.index_of_survey_without_results)
            check = self.repo.check_survey_status(survey_id)
            self.assertTrue(check[2] == [])
    
    def test_check_survey_status_when_no_question_answers_returns_correct(self):
        with self.app.app_context():
            survey_id = self.createSurvey("no_question_answers")
            self.repo.create_question("mock question one", survey_id, self.category_weights)

            check = self.repo.check_survey_status(survey_id)
            self.assertEqual(check[3], ["self.question_text"])
            
            question_two_id = self.repo.create_question("mock question two", survey_id, self.category_weights)
            check = self.repo.check_survey_status(survey_id)
            self.assertEqual(check[3], ["mock question one", "mock question two"])

            self.repo.create_answer("mock answer to question two", 0, question_two_id)
            check = self.repo.check_survey_status(survey_id)
            self.assertEqual(check[3], ["mock question one"])

            self.deleteSurvey(survey_id)
            print(">>>>>>>>>>>>>",self.repo.get_survey(survey_id))
            self.assertTrue(self.repo.get_survey(survey_id) == True)
            
    
    def test_check_survey_status_when_questions_without_categories_returns_correct(self):
        with self.app.app_context():
            survey_id = self.createSurvey("questions_without_categories")
            """self.repo.create_question("mock question one",survey_id, self.category_weights )
            check = self.repo.check_survey_status(survey_id)
            self.assertTrue(check[3] == ["self.question_text"])
            self.repo.create_question("mock question two", survey_id, self.category_weights)
            self.assertTrue(check[3] == ["mock question one", "mock question two"])"""
            self.deleteSurvey(survey_id)
            self.assertTrue(self.repo.get_survey(survey_id) == False)
            

    def test_check_survey_status_when_categories_without_questions_returns_correct(self):
        with self.app.app_context():
            survey_id = self.createSurvey("categories_without_questions")
            self.deleteSurvey(survey_id)
            self.assertTrue(self.repo.get_survey(survey_id) == False)

    def test_check_survey_status_when_no_problems_present_returns_correct(self):
            with self.app.app_context():
                survey_id = self.createSurvey("no_problems_present")
                # [status, no_survey_results, categories_without_results, questions_without_answers, questions_without_categories, categories_without_questions].             
                status_list = self.repo.check_survey_status(survey_id)
                self.assertEquals(len(status_list), 6)
                self.assertEquals(status_list, ['green', False,[],[],[]])
                self.deleteSurvey(survey_id)
                self.assertTrue(self.repo.get_survey(survey_id) == False)
                
