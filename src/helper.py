import json
from secrets import token_hex
from os import path, remove
from glob import glob
from pandas import DataFrame as df
from matplotlib import pyplot as plt
from flask import session
from datetime import datetime

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

def save_question_answer_charts(answer_distribution, user_group="", filter_start_date=None, filter_end_date=None):
    """First clears the static/img/charts directory contents
    if no user group is given and then takes the answer distribution
    table for questions, saves filtered or unfiltered pie charts
    for each question to static/img/charts directory

    Returns:

    If input is none: None
    If input is not none: zip object with q_names and q_ids
    """
    if user_group == "" and filter_start_date is None:
        empty_dir()
    if not answer_distribution:
        return None

    answer_df = df(answer_distribution)
    q_ids = answer_df["question_id"].to_list()
    q_ids = list(dict.fromkeys(q_ids))
    q_names = answer_df["question"].to_list()
    q_names = list(dict.fromkeys(q_names))
    answer_df = answer_df[["question", "answer", "count"]]

    time_range = None
    if filter_start_date is not None:
        filter_start_date = filter_start_date.strftime("%d.%m.%Y, %H:%M")
        filter_end_date = filter_end_date.strftime("%d.%m.%Y, %H:%M")
        time_range = filter_start_date + " - " + filter_end_date

    plot_answer_distribution_for_questions(answer_df, q_names, q_ids, user_group, time_range)

    return zip(q_names, q_ids)

def plot_answer_distribution_for_questions(dataframe:df, q_names: list, q_ids: list, user_group: str, time_range=None):
    """Plots the answer distribution for each question and saves
    the pie chart as .png to static/img/charts directory

    Returns:

    If succeeds: True
    If exception is raised: False
    """
    current_dir = path.dirname(__file__)
    target_dir = path.join(current_dir, "static/img/charts/")
        
    try:
        plt.switch_backend("Agg")
        for q_name, q_id in zip(q_names, q_ids):
            question_to_plot = dataframe[dataframe["question"] == q_name]
            answer_options = question_to_plot["answer"].to_list()
            question_to_plot.plot(kind="pie",
                                labels=answer_options,
                                y="count",
                                autopct="%1.1f%%")
            plt.legend(title="Answer options",
                        loc="upper left",
                        bbox_to_anchor=(0.9, 0, 0, 1))

            if user_group == "" and time_range is None:
                plt.title("All users")
            else:
                plt.title(time_range)
            plt.ylabel("")

            if user_group == "" and time_range is None:
                plt.savefig(target_dir + f"{q_id}.png")
            else:
                plt.savefig(target_dir + f"{q_id}_{user_group}.png")
            plt.close()

    except Exception:
        return False
    return True

def empty_dir():
    """Clears the contents of the target directory"""
    try:
        current_dir = path.dirname(__file__)
        to_remove = path.join(current_dir, "static/img/charts/*.png")
        files_to_remove = glob(to_remove)
        for file in files_to_remove:
            remove(file)
    except OSError:
        return False
    return True
