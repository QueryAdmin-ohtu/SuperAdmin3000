
class SurveyRepository:
    """
    A class for interacting with the survey database
    """

    def __init__(self, db_connection):
        self.db_connection = db_connection

    def authorized_google_login(self, email):
        """ Checks whether a Google account is authorized to access the app.
        """
        sql = "SELECT id FROM \"Admins\" WHERE email=:email"
        result = self.db_connection.session.execute(sql, {"email": email})

        user = result.fetchone()

        if user:
            return True

        return False

    def create_survey(self, name, title, survey, created):
        """ Inserts a survey to table Surveys based
        on given parameters and returns the id """
        sql = """
        INSERT INTO "Surveys"
        (name,"createdAt","updatedAt",title_text,survey_text)
        VALUES (:name, :createdAt, :updatedAt, :title_text, :survey_text)
        RETURNING id """
        values = {
            "name": name,
            "createdAt": created,
            "updatedAt": created,
            "title_text": title,
            "survey_text": survey
        }
        survey_id = self.db_connection.session.execute(sql, values).fetchone()
        self.db_connection.session.commit()
        return survey_id[0]

    def get_survey(self, survey_id):
        """ Looks up survey information with
        id and returns it in a list"""
        sql = """ SELECT * FROM "Surveys" WHERE id=:id """
        survey = self.db_connection.session.execute(sql, {"id": survey_id}).fetchone()
        if not survey:
            return False
        return survey
        
    def get_questions_of_questionnaire(self, questionnaire_id):
        """ Fetches questions of a given questionnaire
        Args:
          questionnaire_id: Id of the questionnaire

        Returns:
          An array containing each question object
        """
        sql = "SELECT * FROM \"Questions\" WHERE \"Questions\".\"surveyId\"=:questionnaire_id"
        result = self.db_connection.session.execute(sql, {"questionnaire_id": questionnaire_id})

        questions = result.fetchall()

        return questions
