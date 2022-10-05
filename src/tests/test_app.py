from views.home import ping


def test_ping(app):
    expected = "pong"
    result = ping()
    assert expected in result

# Robot framework is used for the functional tests (return data of
# GET and POSTS methdods in routes, etc.)
#
# def test_test_page(app, client):
#    expected = "Unauthorized"
#    result = client.get("/test")
#    assert expected in result.text

