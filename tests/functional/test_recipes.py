def test_request_example(client):
    response = client.get("/")
    assert b"My Shopping List" in response.data