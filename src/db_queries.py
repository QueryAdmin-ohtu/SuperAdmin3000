from app import db

# TODO: Create a proper storage for the authorized users
# pylint: disable-next=line-too-long
authorized_google_accounts = ["antti.vainikka36@gmail.com", "jatufin@gmail.com", "me@juan.fi",
                              # pylint: disable-next=line-too-long
                              "niemi.leo@gmail.com", "oskar.sjolund93@gmail.com", "rami.piik@gmail.com", "siljaorvokki@gmail.com"]


def authorized_google_login(email):
    """ Checks whether a Google account is authorized to access the app.
    """
    sql = "SELECT id FROM \"Admins\" WHERE email=:email"
    result = db.session.execute(sql, {"email": email})

    user = result.fetchone()

    if user:
        return True

    return False


def google_login_authorize(email):
    """ Checks whether a Google account is authorized to access the app.
    """
    if email in authorized_google_accounts:
        return True
    return False
