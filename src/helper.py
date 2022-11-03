import json
from secrets import token_hex
from flask import session
from pandas import DataFrame as df
from matplotlib import pyplot as plt
import os

def backdoor_validate_and_login(username, password):
    """ Check if the given username password pair is correct
    If username and password match, a new session will be created
    """
    # TODO: Proper data storage for usernames and password hashes
    if username != "rudolf":
        return False
    if password != "secret":
        return False

    session["csrf_token"] = token_hex(16)
    session["username"] = username
    return True


def update_session(email, first_name, csrf_token_cookie):
    """ Update Flask session variables
    """
    session["email"] = email
    session["username"] = first_name
    session["csrf_token"] = csrf_token_cookie


def clear_session():
    """ Logout the user and clear session properties
    """
    _remove_from_session("email")
    _remove_from_session("username")
    _remove_from_session("csrf_token")


def _remove_from_session(property_key):
    """ Checks if the given property name can be found in the session
    and removes it
    """
    if property_key in session:
        del session[property_key]


def logged_in():
    """ Check if the session is active. This should be always used before
    rendering pages.
    """
    return "username" in session


def current_user():
    """ Returns the username of the currently logged in user
    """
    if not logged_in():
        return None

    return session["username"]


def valid_token(form, tokenname="csrf_token"):
    """ Check if the token send with the form matches with the current
    session.
    """
    if not logged_in():
        return False

    if tokenname not in form:
        return False

    return form[tokenname] == session[tokenname]


def category_weights_as_json(categories: list, form: dict):
    """ Constructs category weights as json based on user input
    Args:
        categories: List of categories. Items on the list are lists containing category id and category name
        form: Dictionary containing the desired category weights

    Returns:
        Category list as serialized json """
    category_list = []
    for category in categories:
        category_dict = {}
        category_dict["category"] = category[1]
        weight = form["cat"+str(category[0])]
        try:
            if not weight:  # no input means zero weight
                weight = 0
            weight = str(weight).replace(",", ".")
            category_dict["multiplier"] = float(weight)
        except ValueError as exc:
            raise ValueError from exc
        category_list.append(category_dict)

    return json.dumps(category_list)


def json_into_dictionary(json_file):
    """ Takes category weights and makes them into
    a dictionary where the keys are the category
    names and the values are the multipliers """
    categories = {}
    for category in json_file:
        categories[category["category"]] = category["multiplier"]
    return categories

def save_question_answer_charts(answer_distribution):
    """Takes the answer distribution table for questions,
    saves pie charts for each question to static/img folder

    Returns:
        q_names: list of question names
        q_ids: list of question id's
    """
    current_dir = os.path.dirname(__file__)
    target_dir = os.path.join(current_dir, "static/img/")

    answer_df = df(answer_distribution)
    q_ids = answer_df["question_id"].to_list()
    q_names = answer_df["question"].to_list()
    answers = answer_df["answer"].to_list()
    answer_df = answer_df[["question", "answer", "count"]]

    for name, q_id in zip(q_names, q_ids):
        df_for_question = answer_df[answer_df["question"] == name]
        df_for_question = df_for_question[["answer", "count"]]
        df_for_question.plot(kind='pie', labels=answers, y='count')
        plt.savefig(target_dir + f"{q_id}.png")

    return q_names, q_ids
