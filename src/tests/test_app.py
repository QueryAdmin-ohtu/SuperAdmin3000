def test_index(app, client):
    expected = "Hello world!"

    result = client.get("/")
    
    assert expected in result.text
