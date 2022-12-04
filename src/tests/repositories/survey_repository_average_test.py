import unittest

from repositories.survey_repository import SurveyRepository

from app import create_app

class TestSurveyRepository(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.repo = SurveyRepository()

    def tearDown(self):
        self.app.db.get_engine(self.app).dispose()

    def createSurvey(self, title):
        """
        Creates a survey with two user groups and three users
            User Groups
                "user_group_one"
                "user_group_two
            Users
                advanced_user_id
                mediocre_user_id
                beginner_user_id
            
        Returns : Dictionary with keys {
            survey_id,
            user_group_1_id,
            user_group_2_id,
            advanced_user_id,
            beginner_user_id}
        """
        survey_id = self.repo.create_survey("Mock Survey", title, "")
        user_group_1_id = self.repo._add_survey_user_group("user_group_one", survey_id)
        user_group_2_id = self.repo._add_survey_user_group("user_group_two", survey_id)
        advanced_user_id = self.repo._add_user(email="Advanced@domain.invalid", group_id=user_group_1_id)
        mediocre_user_id = self.repo._add_user(email="Mediocre@domain.invalid", group_id=user_group_1_id)
        beginner_user_id = self.repo._add_user(email="Beginner@domain.invalid", group_id=user_group_2_id)
       

        return {"survey_id":survey_id,
                "user_group_1_id" : user_group_1_id,
                "user_group_2_id" : user_group_2_id,
                "advanced_user_id": advanced_user_id,
                "mediocre_user_id" : mediocre_user_id,
                "beginner_user_id" : beginner_user_id,
                }

    def test_calculate_average_one_category_no_filters(self):
        with self.app.app_context():
            survey = self.createSurvey("Maths")
            survey_id = survey['survey_id']
            category_math_id = self.repo.create_category(survey_id, "Math", "I'm the operator of my pocket calculator", '[]')
            question_id = self.repo.create_question(
                "How is the average calculated", survey_id,
                '[{"category": "Math", "multiplier": 1.0}]')

            answer_one_good_id = self.repo.create_answer(
                "Calculate sum of elements and divide by their number", 5, question_id)
            
            answer_one_bad_id = self.repo.create_answer(
                "Next question, please", 0, question_id)
            self.repo._add_user_answers(
                survey['advanced_user_id'], [answer_one_good_id])
            self.repo._add_user_answers(
                survey['mediocre_user_id'], [answer_one_good_id])
            self.repo._add_user_answers(
                survey['beginner_user_id'], [answer_one_bad_id])

            category_averages = self.repo.calculate_average_scores_by_category(survey_id)
            self.assertEquals(len(category_averages), 1)
            self.assertEquals(category_averages, [(category_math_id, 'Math', 3.33)])

    def test_calculate_averages_of_two_categories_with_one_question_each(self):
         with self.app.app_context():
            survey = self.createSurvey("Two Averages")
            survey_id = survey['survey_id']
            category_A_id = self.repo.create_category(survey_id, "A", "", '[]')
            category_B_id = self.repo.create_category(survey_id, "B", "", '[]')
            question_A_id = self.repo.create_question(
                "How is the average calculated", survey_id,
                '[{"category": "A", "multiplier": 1.0}]')
            question_B_id = self.repo.create_question(
                "How is the average calculated", survey_id,
                '[{"category": "B", "multiplier": 1.0}]')
            answer_A_good_id = self.repo.create_answer("Good", 10, question_A_id)
            answer_A_bad_id = self.repo.create_answer("None", 0, question_A_id)
            answer_B_good_id = self.repo.create_answer("Good", 10, question_B_id)
            answer_B_bad_id = self.repo.create_answer("None", 0, question_B_id)
            
            self.repo._add_user_answers(
                survey['advanced_user_id'], [answer_A_good_id, answer_B_good_id])
            self.repo._add_user_answers(
                survey['mediocre_user_id'], [answer_A_bad_id, answer_B_bad_id])
            self.repo._add_user_answers(
                survey['beginner_user_id'], [answer_A_bad_id])
            averages = self.repo.calculate_average_scores_by_category(survey_id)
            
            self.assertEquals(averages, [(category_A_id,'A', 3.33), (category_B_id, 'B', 5.0)])

   
