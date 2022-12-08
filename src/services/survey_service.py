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
        survey_id = self.survey_repository.create_survey(
            name, title, description)
        if survey_id:
            survey_result_text = "Your skills in this topic are excellent!"
            cutoff_from_maxpts = 1.0
            self.create_survey_result(survey_id,
                                      survey_result_text,
                                      cutoff_from_maxpts)

        return survey_id

    def get_survey(self, survey_id: str):
        """
        Returns survey from the repository

        Args:
            survey_id: Db id of survey

        Returns:
            If succeeds: Survey (fields: id, name, createdAt, updatedAt, title_text, survey_text)
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

        Returns: A list containing:
            [0] survey id
            [1] title,
            [2] question count
            [3] submission count
            [4] survey status
        """

        surveys = self.survey_repository.get_all_surveys()
        result = []

        for row in surveys:
            survey = list(row)
            survey_id = survey[0]
            status = self.check_survey_status(survey_id)
            survey.append(status)
            result.append(survey)

        return result

    def get_questions_of_survey(self, survey_id: str):
        """ Fetches questions of a given survey
        Args:
          survey_id: Id of the survey

        Returns:
          An array containing each question object;
          question object fields: id, text, surveyId, category_weights, createdAt, updatedAt
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
            raise UserInputError("Missing required details of survey")

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
        categories = self.survey_repository.get_categories_of_survey(survey_id)

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

    def update_question(self, question_id: int, text: str, category_weights: str, original_answers, new_answers):
        """ Updates a question if changes have been made and returns true.
        If no changes have been made, nothing changes and false is returned """
        return self.survey_repository.update_question(
            question_id, text, category_weights, original_answers, new_answers)

    def get_question(self, question_id):
        """Gets the text, survey id, category weights, and the
        time of creation of a question based on the questions id """
        return self.survey_repository.get_question(question_id)

    def get_question_answers(self, question_id):
        """Gets the id:s, texts and points of the answers
        from the question specified by the id given """
        return self.survey_repository.get_question_answers(question_id)

    def get_user_answers(self, answer_id):
        "" """ Gets the id, user id and both question_answer_id AND Question_answer_id of
        the answer determined by the given answer_id """
        return self.survey_repository.get_user_answers(answer_id)

    def create_category(self, survey_id: str, name: str, description: str, content_links: list):
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
        category_id = self.survey_repository.create_category(
            survey_id, name, description, content_links)
        if category_id:
            category_result_text = "Your skills in this topic are excellent!"
            cutoff_from_maxpts = 1.0
            self.create_category_result(
                category_id,
                survey_id,
                category_result_text,
                cutoff_from_maxpts
            )

        return category_id

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

    def update_category(self, category_id: str, content_links: list, name=None, description=None,):
        """
        Updates category information.

        Args:
            category_id: database if of the category to be updated
            content_links: New content links related to the category
            name: New name of the category
            description: New description of the category

        Returns:
            If succeeds: The DB id of the created category
            If not: False
        """

        if name is None:
            category = self.get_category(category_id)
            name = category[1]
        if description is None:
            category = self.get_category(category_id)
            description = category[2]

        return self.survey_repository.update_category(category_id, content_links, name, description)

    def delete_category_in_questions(self, question_ids: list, questions_weights: list):
        """ Deletes the category from category weights
        in the questions from the repository """
        for question_id, weights in zip(question_ids, questions_weights):
            self.survey_repository.remove_category_from_question(
                question_id,
                weights
            )
        return True

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

    def delete_category_results_for_category(self, category_id, survey_id):
        """ Deletes all category results for the given
        category from the repository """
        self.update_category_and_survey_updated_at(category_id, survey_id)
        return self.survey_repository.delete_category_results_of_category(category_id)

    def update_category_and_survey_updated_at(self, category_id, survey_id):
        """ Updates the updatedAt of a category and survey based on category_id
        """
        self.survey_repository.update_category_and_survey_updated_at(
            category_id, survey_id)

    def create_category_result(self, category_id: int, survey_id: int, text: str, cutoff_from_maxpts: float):
        """Create a new category result

        Returns id of category result"""
        self.update_category_and_survey_updated_at(category_id, survey_id)
        return self.survey_repository.create_category_result(category_id, text, cutoff_from_maxpts)

    def get_category_results_from_category_id(self, category_id):
        return self.survey_repository.get_category_results_from_category_id(category_id)

    def create_survey_result(self, survey_id, text, cutoff_from_maxpoints):
        """Create a new survey result

        Returns id of survey result
        """
        return self.survey_repository.create_survey_result(survey_id, text, cutoff_from_maxpoints)

    def get_survey_results(self, survey_id):
        """Fetch the results of the given survey

        Returns a table with columns: id, text, cutoff_from_maxpoints
        """
        return self.survey_repository.get_survey_results(survey_id)

    def delete_survey_result(self, result_id):
        """ Deletes the given survey result
        """

        return self.survey_repository.delete_survey_result(result_id)

    def update_survey_results(self, original_results, new_results, survey_id):
        """Updates the original results of a survey to new ones"""
        return self.survey_repository.update_survey_results(original_results, new_results, survey_id)

    def delete_category_result(self, category_result_id, category_id, survey_id):
        """ Deletes the category result given as parameter
        """
        self.update_category_and_survey_updated_at(category_id, survey_id)
        return self.survey_repository.delete_category_result(category_result_id)

    def update_category_results(self, original_results, new_results, survey_id, category_id):
        """Updates the original results of a survey to new ones"""
        self.update_category_and_survey_updated_at(category_id, survey_id)
        return self.survey_repository.update_category_results(original_results, new_results, survey_id)

    def check_survey_status(self, survey_id):
        """Check the survey status: Returns a list containing survey status
        and detailed information about the checks

        [0]    status_color  : (str) 'red','yellow' or 'green',
        [1]    no_survey_results : (bool),
        [2]    no_categories : (bool),
        [3]    unrelated_categories_in_weights : (list) [category names]
        [4]    no_questions : (bool),
        [5]    questions_without_answers :(list) [question names],
        [6]    questions_without_categories :(list) [category names],
        [7]    categories_without_questions : (list) [category names]
        [8]    categories_without_results :
                (dictionary) {question_id: [category names]},
        """

        survey_status_array = self.survey_repository.check_survey_status(survey_id)
        survey_status_dictionary = {
            "status_color": survey_status_array[0],
            "no_survey_results": survey_status_array[1],
            "no_categories": survey_status_array[2],
            "unrelated_categories_in_weights": survey_status_array[3],
            "no_questions": survey_status_array[4],
            "questions_without_answers": survey_status_array[5],
            "questions_without_categories": survey_status_array[6],
            "categories_without_questions": survey_status_array[7],
            "categories_without_results": survey_status_array[8]
        }

        return survey_status_dictionary


survey_service = SurveyService(SurveyRepository())
