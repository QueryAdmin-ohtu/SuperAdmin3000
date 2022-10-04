from datetime import datetime
import re

class UserInputError(Exception):
    pass


class SurveyService:
    """
    A class for safely interacting with the survey repository
    """

    def __init__(self, survey_repository):
        self.survey_repository = survey_repository

    def check_if_authorized_google_login(self, email):
        """
        Checks if a given Google account is authoried to access the app.

        Args:
            email: Google account email address to check

        Returns:
            Boolean value
        """
        try:
            if self._validate_email_address(email):
                return self.survey_repository.authorized_google_login(email)
        except UserInputError:
            return False

    def create_survey(self, name: str, title: str, description: str):
        """
        Creates a new survey with given information

        Args:
            name: Name of survey
            title: Survey title
            description: A description about the survey

        Returns:
            If succeeds: The DB id of the created survey
        """

        self._validate_survey_details(name, title, description)

        created = datetime.now()
        return self.survey_repository.create_survey(name, title, description, created)

    def get_survey(self, survey_id: str):
        """
        Returns survey from the repository

        Args:
            survey_id: Db id of survey

        Returns:
            If succeeds: Survey
            Not found: False
        """

        return self.survey_repository.get_survey(survey_id)

    def get_questions_of_survey(self, survey_id: str):
        """ Fetches questions of a given questionnaire
        Args:
          questionnaire_id: Id of the questionnaire

        Returns:
          An array containing each question object
        """
        return self.survey_repository.get_questions_of_questionnaire(survey_id)

    def _validate_survey_details(self, name: str, title: str, description: str):
        """ Checks given survey details
        Returns:
            True if inputs are ok

        Raises:
            UserInputError: If survey is missing required details

        """
        if len(name) < 1 or len(title) < 1 or len(description) < 1:
            raise UserInputError("Missing required information of survey")
            
        if len(name) > 1000 or len(title) > 1000 or len(description) > 1000:
            raise UserInputError("Survey input is too long")

        return True

    def _validate_email_address(self, email_address: str):
        """ Check if given email address
        Returns:
            True if inputs are ok

        Raises:
            UserInputError: If email address if flawed
        """

        regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

        if re.fullmatch(regex, email_address):
            return True

        raise UserInputError("Given email address is flawed")
