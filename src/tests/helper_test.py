import pytest

import os
from app import create_app
import helper
from pandas import DataFrame as df
from glob import glob
from os import path
from datetime import datetime


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


def test_backdoor_validate_and_login_with_invalid_password(app):
    with app.test_request_context() as context:
        response = helper.backdoor_validate_and_login("rudolf", "wrong")

        assert response == False
        assert "username" not in context.session
        assert "csrf_token" not in context.session


def test_backdoor_validate_and_login_with_invalid_username(app):
    with app.test_request_context() as context:
        response = helper.backdoor_validate_and_login("wrong", "secret")

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


def test_save_question_charts_returns_correct_object_when_given_answer_dist_with_no_user_group():
    test_distribution = {
        "question_id":
            [29, 29, 30, 30],
        "question":
            ["Describe the size of your ears",
             "Describe the size of your ears",
             "Where do you prefer to hang out?",
             "Where do you prefer to hang out?"],
        "answer_id":
            [42, 43, 44, 45],
        "answer":
            ["Huge",
             "Nonexistent",
             "Forest",
             "Savannah"],
        "count":
            [2, 1, 1, 2]
    }
    return_type = helper.save_question_answer_charts(test_distribution)
    result = list(return_type)
    expected_result = list(
        zip(
            ["Describe the size of your ears", "Where do you prefer to hang out?"],
            [29, 30]
        )
    )
    assert result == expected_result
    assert type(return_type) == zip


def test_save_question_charts_empties_dir_with_no_user_group():
    result = helper.save_question_answer_charts(None)
    empty_dir_test()


def test_save_question_charts_returns_none_with_none_input():
    result = helper.save_question_answer_charts(None)
    assert result is None


def test_plot_answer_dist_for_questions_returns_true_if_no_exception_raised():
    test_data = {
        "question":
            ["Describe the size of your ears",
             "Describe the size of your ears",
             "Where do you prefer to hang out?",
             "Where do you prefer to hang out?"],
        "answer":
            ["Huge",
             "Nonexistent",
             "Forest",
             "Savannah"],
        "count":
            [2, 1, 1, 2]
    }
    q_names = ["Describe the size of your ears",
               "Describe the size of your ears",
               "Where do you prefer to hang out?",
               "Where do you prefer to hang out?"]
    q_ids = [42, 42, 43, 43]
    test_df = df(data=test_data)
    result = helper.plot_answer_distribution_for_questions(
        test_df, q_names, q_ids, "")
    assert result == True


def test_plot_answer_dist_for_questions_returns_false_when_exception_raised():
    q_names = ["Describe the size of your ears",
               "Describe the size of your ears",
               "Where do you prefer to hang out?",
               "Where do you prefer to hang out?"]
    q_ids = [42, 42, 43, 43]
    result = helper.plot_answer_distribution_for_questions(
        [1, 2, 3], q_names, q_ids, "")
    assert result == False


def test_plot_answer_dist_for_questions_creates_png_files_without_filters():
    test_data = {
        "question":
            ["Describe the size of your ears",
             "Describe the size of your ears",
             "Where do you prefer to hang out?",
             "Where do you prefer to hang out?"],
        "answer":
            ["Huge",
             "Nonexistent",
             "Forest",
             "Savannah"],
        "count":
            [2, 1, 1, 2]
    }
    q_names = ["Describe the size of your ears",
               "Describe the size of your ears",
               "Where do you prefer to hang out?",
               "Where do you prefer to hang out?"]
    q_ids = [42, 42, 43, 43]
    test_df = df(data=test_data)
    helper.plot_answer_distribution_for_questions(test_df, q_names, q_ids, "")

    current_dir = path.dirname(__file__)
    root_dir = path.dirname(current_dir)
    charts_path = path.join(root_dir, "static/img/charts/*.png")
    list_of_file_paths = sorted(glob(charts_path))
    files = list(map(path.basename, list_of_file_paths))

    assert files[0] == "42.png"
    assert files[1] == "43.png"


def test_plot_answer_dist_for_questions_creates_png_files_with_all_filters():
    helper.empty_dir()
    test_data = {
        "question":
            ["Describe the size of your ears",
             "Describe the size of your ears",
             "Where do you prefer to hang out?",
             "Where do you prefer to hang out?"],
        "answer":
            ["Huge",
             "Nonexistent",
             "Forest",
             "Savannah"],
        "count":
            [2, 1, 1, 2]
    }
    q_names = ["Describe the size of your ears",
               "Describe the size of your ears",
               "Where do you prefer to hang out?",
               "Where do you prefer to hang out?"]
    q_ids = [42, 42, 43, 43]
    test_df = df(data=test_data)
    filter_start_date = datetime.now().strftime("%d.%m.%Y, %H:%M")
    filter_end_date = datetime.now().strftime("%d.%m.%Y, %H:%M")
    time_range = filter_start_date + " - " + filter_end_date

    helper.plot_answer_distribution_for_questions(
        test_df, q_names, q_ids, "test", time_range)

    current_dir = path.dirname(__file__)
    root_dir = path.dirname(current_dir)
    charts_path = path.join(root_dir, "static/img/charts/*.png")
    list_of_file_paths = sorted(glob(charts_path))
    files = list(map(path.basename, list_of_file_paths))

    assert files[0] == "42_test.png"
    assert files[1] == "43_test.png"


def test_plot_answer_dist_for_questions_creates_png_files_with_only_time_filter():
    helper.empty_dir()
    test_data = {
        "question":
            ["Describe the size of your ears",
             "Describe the size of your ears",
             "Where do you prefer to hang out?",
             "Where do you prefer to hang out?"],
        "answer":
            ["Huge",
             "Nonexistent",
             "Forest",
             "Savannah"],
        "count":
            [2, 1, 1, 2]
    }
    q_names = ["Describe the size of your ears",
               "Describe the size of your ears",
               "Where do you prefer to hang out?",
               "Where do you prefer to hang out?"]
    q_ids = [42, 42, 43, 43]
    test_df = df(data=test_data)
    filter_start_date = datetime.now().strftime("%d.%m.%Y, %H:%M")
    filter_end_date = datetime.now().strftime("%d.%m.%Y, %H:%M")
    time_range = filter_start_date + " - " + filter_end_date

    helper.plot_answer_distribution_for_questions(
        test_df, q_names, q_ids, "", time_range)

    current_dir = path.dirname(__file__)
    root_dir = path.dirname(current_dir)
    charts_path = path.join(root_dir, "static/img/charts/*.png")
    list_of_file_paths = sorted(glob(charts_path))
    files = list(map(path.basename, list_of_file_paths))

    assert files[0] == "42_.png"
    assert files[1] == "43_.png"


def test_empty_dir_deletes_files():
    empty_dir_test()


def empty_dir_test():
    with open('src/static/img/charts/image.png', 'w') as f:
        f.write('IMAGE HERE')

    file_count_before = 0
    for root_dir, cur_dir, files in os.walk("src/static/img/charts/"):
        file_count_before += len(files)

    helper.empty_dir()

    file_count_after = 0
    for root_dir, cur_dir, files in os.walk("src/static/img/charts/"):
        file_count_after += len(files)

    assert file_count_before > 1
    assert file_count_after == 1


def test_check_cutoff_points():
    no_one = ["0.5", "0.7", "0.1"]
    duplicates = ["0.5", "0.5", "0.1", "1"]
    not_in_range = ["0.5", "2", "-0.3", "1.0"]
    empty_cutoff = ["0.5", "0.2", "", "1"]
    all_good_man = ["0.9", "0.5", "0.1", "1"]
    assert helper.check_cutoff_points(
        no_one) == "There must be a cutoff from maximum with a value of 1.0"
    assert helper.check_cutoff_points(
        duplicates) == "There must not be any identical cutoff values"
    assert helper.check_cutoff_points(
        not_in_range) == "Cutoff values must be between 0 and 1"
    assert helper.check_cutoff_points(
        empty_cutoff) == "There is a result without a cutoff value"
    assert helper.check_cutoff_points(all_good_man) == "Correct"


def test_return_true_if_category_weight_is_only_non_zero_for_question():
    weight_json = [{"category": "Category 1", "multiplier": 0},
                   {"category": "Category 2", "multiplier": 1},
                   {"category": "Category 3", "multiplier": 0},
                   {"category": "Category 4", "multiplier": 0},
                   {"category": "Category 5", "multiplier": 0}]
    question = [2,
                'Question 2',
                1,
                weight_json,
                datetime.now(),
                datetime.now()]
    cat_name = "Category 2"
    result = helper.only_non_zero_weight_for_question(question, cat_name)
    assert result == True


def test_return_false_if_category_weight_is_not_only_non_zero_for_question():
    weight_json = [{"category": "Category 1", "multiplier": 0},
                   {"category": "Category 2", "multiplier": 0},
                   {"category": "Category 3", "multiplier": 1},
                   {"category": "Category 4", "multiplier": 0},
                   {"category": "Category 5", "multiplier": 0}]
    question = [2,
                'Question 2',
                1,
                weight_json,
                datetime.now(),
                datetime.now()]
    cat_name = "Category 2"
    result = helper.only_non_zero_weight_for_question(question, cat_name)
    assert result == False


def test_category_required_by_contains_correct_question_names():
    weight_json = [{"category": "Category 1", "multiplier": 0},
                   {"category": "Category 2", "multiplier": 1},
                   {"category": "Category 3", "multiplier": 0},
                   {"category": "Category 4", "multiplier": 0},
                   {"category": "Category 5", "multiplier": 0}]
    weight_json_2 = [{"category": "Category 1", "multiplier": 0},
                     {"category": "Category 2", "multiplier": 1},
                     {"category": "Category 3", "multiplier": 1},
                     {"category": "Category 4", "multiplier": 0},
                     {"category": "Category 5", "multiplier": 0}]
    requires_cat = [2,
                    "Question 2",
                    1,
                    weight_json,
                    datetime.now(),
                    datetime.now()]
    doesnt_require_cat = [3,
                          "Question 3",
                          1,
                          weight_json_2,
                          datetime.now(),
                          datetime.now()]
    requires_cat_2 = [4,
                      "Question 4",
                      1,
                      weight_json,
                      datetime.now(),
                      datetime.now()]
    questions = [requires_cat,
                 doesnt_require_cat,
                 requires_cat_2]

    result = helper.questions_where_given_category_is_required(
        questions,
        "Category 2"
    )
    assert result == ["Question 2", "Question 4"]


def test_category_is_removed_from_weights():
    original_weights = [{"category": "dog", "multiplier": "1"}, {
        "category": "cat", "multiplier": "0"}]
    result = helper.updated_category_weights_as_json(
        original_weights,
        "cat"
    )
    assert result == '[{"category": "dog", "multiplier": "1"}]'


def test_updated_category_weights_as_json_returns_none_with_empty_weights():
    result = helper.updated_category_weights_as_json(
        None,
        "cat"
    )
    assert result is None


def test_updated_question_ids_and_weights_removes_cat_from_all_weights():
    questions = [
        (
            1,
            None,
            None,
            [{"category": "dog", "multiplier": "1"}, {
                "category": "cat", "multiplier": "1"}],
            None,
            None
        ),
        (
            2,
            None,
            None,
            [{"category": "dog", "multiplier": "1"}, {"category": "cat",
                                                      "multiplier": "0"}, {"category": "bird", "multiplier": "3"}],
            None,
            None
        )
    ]
    question_ids, cat_weights = helper.updated_question_ids_and_weights(
        questions,
        "cat"
    )
    assert question_ids == [1, 2]
    assert cat_weights == [
        '[{"category": "dog", "multiplier": "1"}]',
        '[{"category": "dog", "multiplier": "1"}, {"category": "bird", "multiplier": "3"}]'
    ]
