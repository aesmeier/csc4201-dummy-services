import pytest
import main


@pytest.fixture
def client():
    main.app.testing = True
    return main.app.test_client()


def test_successful_charge(client):
    r = client.post("/charges", json={
        "amount": 49.99,
        "card": {"number": "4111111111111111"}
    })
    assert r.status_code == 200
    assert "transaction_id" in r.get_json()


def test_declined_card(client):
    r = client.post("/charges", json={
        "amount": 49.99,
        "card": {"number": "4111111110000"}
    })
    assert r.status_code == 402


def test_missing_amount(client):
    r = client.post("/charges", json={"card": {"number": "4111111111111111"}})
    assert r.status_code == 400


def test_invalid_card_number(client):
    r = client.post("/charges", json={"amount": 10, "card": {"number": "123"}})
    assert r.status_code == 402