def test_index(app, client):
    expected = "You are not logged in"

    result = client.get("/")

    assert expected in result.text
