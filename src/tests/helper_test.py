import pytest

from app import create_app
import helper


@pytest.fixture()
def app():
    app = create_app()
    app.secret_key = "testkey"

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def test_backdoor_validate_and_login_with_valid_credentials(app):
    with app.test_request_context() as context:
        response = helper.backdoor_validate_and_login("rudolf", "secret")

        assert response == True
        assert context.session["username"] == "rudolf"
        assert context.session["csrf_token"]


def test_backdoor_validate_and_login_with_invalid_credentials(app):
    with app.test_request_context() as context:
        response = helper.backdoor_validate_and_login("rudolf", "wrong")

        assert response == False
        assert "username" not in context.session
        assert "csrf_token" not in context.session


def test_update_session(app):
    with app.test_request_context() as context:
        helper.update_session("user@mail", "user", "token")

        assert context.session["email"] == "user@mail"
        assert context.session["username"] == "user"
        assert context.session["csrf_token"] == "token"


def test_clear_session(app):
    with app.test_request_context() as context:
        context.session["email"] = "user@mail"
        context.session["username"] = "user"
        context.session["csrf_token"] = "token"

        helper.clear_session()
        assert "email" not in context.session
        assert "username" not in context.session
        assert "csrf_token" not in context.session


def test_logged_in_when_logged_in(app):
    with app.test_request_context() as context:
        context.session["username"] = "user"

        response = helper.logged_in()

        assert response


def test_logged_in_when_not_logged_in(app):
    with app.test_request_context() as context:
        response = helper.logged_in()

        assert not response


def test_valid_token_succeeds_if_username_and_token_are_present(app):
    with app.test_request_context() as context:
        form = {"csrf_token": "tokenX"}

        context.session["username"] = "user"
        context.session["csrf_token"] = "tokenX"

        assert helper.valid_token(form)


def test_valid_token_fails_if_username_and_token_are_not_present(app):
    with app.test_request_context() as context:
        form = {"csrf_token": "tokenX"}

        if "username" in context.session:
            del context.session["username"]

        context.session["csrf_token"] = "tokenX"

        assert not helper.valid_token(form)

        context.session["username"] = "user"
        context.session["csrf_token"] = "tokenY"

        assert not helper.valid_token(form)

        context.session["username"] = None
        context.session["csrf_token"] = None

        assert not helper.valid_token(form)


def test_category_weights_as_json_returns_json():
    categories = [[1, "Category 1"], [2, "Category 2"]]
    form = {"cat1": 10, "cat2": 20}

    correct_json = '[{"category": "Category 1", "multiplier": 10.0}, {"category": "Category 2", "multiplier": 20.0}]'
    result = helper.category_weights_as_json(categories, form)

    assert result == correct_json


def test_json_as_dictionary():
    json = [{"category": "Category 1", "multiplier": 10.0},
            {"category": "Category 2", "multiplier": 20.0}]
    result = helper.json_into_dictionary(json)
    result = [result["Category 1"], result["Category 2"]]
    assert result == [10.0, 20.0]
