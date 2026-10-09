import pytest
import main


@pytest.fixture
def client():
    main.app.testing = True
    return main.app.test_client()


def test_send_email(client):
    r = client.post("/emails/user1", json={"order_id": "abc123"})
    assert r.status_code == 200
    assert r.get_json()["status"] == "sent"