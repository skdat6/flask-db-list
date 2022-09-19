import pytest


@pytest.mark.routes
def test_request_home_page(client):
    response = client.get("/")
    assert b"Shopping List" in response.data


@pytest.mark.routes
def test_request_add_page(client):
    response = client.get("/add")
    assert b"Add New Item" in response.data


@pytest.mark.routes
def test_request_edit_price_page(client):
    response = client.get("/edit")
    assert b"Edit Price" in response.data

