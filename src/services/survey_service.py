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

        return self.survey_repository.create_survey(name, title, description)

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

    def delete_answer_from_question(self, answer_id):
        """ Removes an answer from a question.
        Args:
            answer_id: Db id of answer
        Returns:
            If succeeds: True
            Not found: False
        """

        return self.survey_repository.delete_answer_from_question(answer_id)

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

    def get_category(self, category_id: str):
        """
        Returns category from the repository

        Args:
            category_id: Db id of category

        Returns:
            If succeeds: Survey
            Not found: False
        """

        return self.survey_repository.get_category(category_id)

    def get_categories_of_survey(self, survey_id: str):
        """
        Returns categories of the given survey from the repository

        Args:
            survey_id: Db id of the survey

        Returns:
            List of category_id's
        """
        categories=self.survey_repository.get_categories_of_survey(survey_id)

        return categories
    
    def create_question(self, text: str, survey_id: int, category_weights: str):
        """
        Creates a new questions with given information.

        Args:
            text: Content of the question
            survey_id: Id of the survey that the question is related to
            category_weights: json-formatted string containing the category weights of the question

        Returns:
            If succeeds: The DB id of the created question
        """
        return self.survey_repository.create_question(text, survey_id, category_weights)

    def create_answer(self, text: str, points: int, question_id: int):
        """
        Creates a new questions with given information.

        Args:
            text: Content of the answer
            points: The numerical value which is multiplied by the category_weights of the question
            question_id: Id of the question that the answer is related to

        Returns:
            If succeeds: The DB id of the created answer
        """
        return self.survey_repository.create_answer(text, points, question_id)

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

    def update_question(self, question_id: int, text: str, category_weights: str):
        """ Updates a question if changes have been made and returns true.
        If no changes have been made, nothing changes and false is returned """
        return self.survey_repository.update_question(question_id, text, category_weights)

    def get_question(self, question_id):
        """Gets the text, survey id, category weights, and the
        time of creation of a question based on the questions id """
        return self.survey_repository.get_question(question_id)

    def get_question_answers(self, question_id):
        """Gets the id:s, texts and points of the answers
        from the question specified by the id given """
        return self.survey_repository.get_question_answers(question_id)

    def create_category(self, survey_id:str, name: str, description: str, content_links: list):
        """
        Creates a new category.

        Args:
            name: Name of the category
            survey_id: Id of the survey that the category is linked to
            description: Description of the category
            content_links: Content links related to the category

        Returns:
            If succeeds: The DB id of the created category
            If not: None
        """
        return self.survey_repository.create_category(survey_id, name, description, content_links)

    def add_admin(self, email: str):
        """
        Add the given email address to authorized users list

        Args:
            email: Email address of the authorized user

        Returns:
            If succeeds: The DB id of the authorized user
        """
        try:
            if self._validate_email_address(email):
                admin_id = self.survey_repository.add_admin(email)
                return admin_id
        except UserInputError:
            return None

    def get_all_admins(self):
        """
        Fetch all users authorized to use the application

        Returns:
            List of tuples with each tuple containing the
            id and email for each user """
        return self.survey_repository.get_all_admins()

    def update_category(self, category_id: str, name: str, description: str, content_links: list):
        """
        Updates category information.

        Args:
            category_id: database if of the category to be updated
            name: New name of the category
            description: New description of the category
            content_links: New content links related to the category

        Returns:
            If succeeds: The DB id of the created category
            If not: False
        """
        return self.survey_repository.update_category(category_id, name, description, content_links)

    def delete_category(self, category_id: str):
        """
        Deletes category from the repository

        Args:
            category_id: Db id of the category

        Returns:
            If succeeds: True
            If not: Database exception
        """

        return self.survey_repository.delete_category(category_id)


survey_service = SurveyService(SurveyRepository())
