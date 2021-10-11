from app.tests.client import client
from app.tests.utils.users import IntegrationUsers, UserGenerator
from fastapi.security import OAuth2PasswordRequestForm

class TestAuth:

    @classmethod
    def setup_class(cls):
        cls.user_generator = UserGenerator()
        cls.mock_users = cls.user_generator.generate_users(10)

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self):
        IntegrationUsers.clear_users_table()

    def teardown_method(self):
        IntegrationUsers.clear_users_table()

    def test_auth_users(self):
        """
        Tests for successful token retrieval for 10 authenticated
        mock users
        """
        self.test_create_users()
        for mock_user in self.mock_users:
            self.auth_user_test(mock_user['email'], mock_user['password'])

    def test_create_users(self):
        """
        Tests creation (and retrieval) of 10 mock users
        """
        for mock_user in self.mock_users:
            self.create_user_test(mock_user)

    def auth_user_test(self, username, password):
        res = client.post(
            '/token',
            data={"username": username, "password": password}
        )
        assert res.status_code == 200
        data = res.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def create_user_test(self, user_info: dict):
        res = client.post(
            '/user/',
            json={"email": user_info['email'], "password": user_info['password']},
        )
        assert res.status_code == 200
        data = res.json()
        assert data["email"] == user_info['email']
        assert "id" in data

        user_id = data["id"]
        res = client.get(f"/user/{user_id}")
        assert res.status_code == 200
        data = res.json()
        assert data["email"] == user_info['email']
        assert data["id"] == user_id
