import pytest


@pytest.mark.buttons
def test_request_delete(client):
    response = client.get("/")
    assert b"Delete" in response.data


@pytest.mark.buttons
def test_request_edit(client):
    response = client.get("/")
    assert b"Edit Price" in response.data


@pytest.mark.buttons
def test_request_add_new(client):
    response = client.get("/")
    assert b"Add New Item" in response.data

