from flask import session
from secrets import token_hex
from app import db

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
    session["email"] = email
    session["username"] = first_name
    session["csrf_token"] = csrf_token_cookie


def clear_session():
    """ Logout the user and clear session properties
    """
    _remove_from_session("csrf_token")
    _remove_from_session("username")


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


def valid_token(form, tokenname="csrf_token"):
    """ Check if the token send with the form matches with the current
    session.
    """
    if not logged_in():
        return False

    if tokenname not in form:
        return False
    
    return form[tokenname] == session[tokenname]
