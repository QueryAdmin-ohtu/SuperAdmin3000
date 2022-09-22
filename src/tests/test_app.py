from app import _google_login_authorize, authorized_google_accounts


def test_index(app, client):
    expected_1 = "You are not logged in"
    expected_2 = "Google account"
    result = client.get("/")
    assert expected_1 in result.text
    assert expected_2 in result.text


def test_backdoor(app, client):
    expected = "username"
    result = client.get("/backdoor")
    assert expected in result.text


def test_google_login_authorize(app):
    assert not _google_login_authorize("xxx")
    assert _google_login_authorize(authorized_google_accounts[0])


def test_test_page(app, client):
    expected = "Unauthorized"
    result = client.get("/test")
    assert expected in result.text
