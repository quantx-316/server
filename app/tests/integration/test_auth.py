from app.tests.client import client
from app.tests.utils.users import IntegrationUsers


class TestAuth:

    def setup_method(self):
        IntegrationUsers.clear_users_table()

    def teardown_method(self):
        IntegrationUsers.clear_users_table()

    def test_create_user(self):
        res = client.post(
            '/user/',
            json={"email": "fake@example.com", "password": "password"},
        )
        assert res.status_code == 200
        data = res.json()
        assert data["email"] == "fake@example.com"
        assert "id" in data

        user_id = data["id"]
        res = client.get(f"/user/{user_id}")
        assert res.status_code == 200
        data = res.json()
        assert data["email"] == "fake@example.com"
        assert data["id"] == user_id
