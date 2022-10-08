from datetime import datetime
import re
from repositories.survey_repository import SurveyRepository


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
            return False
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

    def delete_survey(self, survey_id: str):
        """
        Deletes survey from the repository

        Args:
            survey_id: Db id of survey

        Returns:
            If succeeds: True
            If not: False
        """

        return self.survey_repository.delete_survey(survey_id)

    def delete_question_from_survey(self, question_id: str):
        """ Removes a question from a survey.
        Args:
            question_id: Db id of question
        Returns:
            If succeeds: True
            Not found: False
        """

        return self.survey_repository.delete_question_from_survey(question_id)

    def get_all_surveys(self):
        """ Fetches all surveys, counts the questions
        for each survey and the amount of submissions
        related to the survey returning a list

        Returns: Array containing the survey id, title,
        question count and submission count """

        return self.survey_repository.get_all_surveys()

    def get_questions_of_survey(self, survey_id: str):
        """ Fetches questions of a given survey
        Args:
          survey_id: Id of the survey

        Returns:
          An array containing each question object
        """
        return self.survey_repository.get_questions_of_survey(survey_id)

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

        regex = re.compile(
            r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

        if re.fullmatch(regex, email_address):
            return True

        raise UserInputError("Given email address is flawed")

    def get_all_categories(self):
        """ Fetches all categories
        Args:
          None

        Returns:
            Array containing id, name, description and content_links of each category """

        return self.survey_repository.get_all_categories()

    def create_question(self, text: str, survey_id: int, category_weights: str, time: datetime):
        """
        Creates a new questions with given information.

        Args:
            text: Content of the question
            survey_id: Id of the survey that the question is related to
            category_weights: json-formatted string containing the category weights of the question

        Returns:
            If succeeds: The DB id of the created question
        """
        return self.survey_repository.create_question(text, survey_id, category_weights, time)


    def edit_survey(self, survey_id: str, name: str, title: str, description: str):
        """
        Edits existing survey with the given information.

        Args:
            survey_id: Id of the survey to edit
            name: Name for the survey
            title: Title for the survey
            description: Survey text

        Returns:
            If succeeds: The DB id of the updated survey
        """
        self._validate_survey_details(name, title, description)

        return self.survey_repository.edit_survey(survey_id, name, title, description)

    def update_question(self, question_id: int, text: str, category_weights: str, updated: datetime):
        """ Updates a question if changes have been made and returns true.
        If no changes have been made, nothing changes and false is returned """
        return self.survey_repository.update_question(question_id, text, category_weights, updated)

    def get_question(self, question_id):
        """Gets the text, survey id, category weights, and the
        time of creation of a question based on the questions id """
        return self.survey_repository.get_question(question_id)


survey_service = SurveyService(SurveyRepository())
