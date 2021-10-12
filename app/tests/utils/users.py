import app.tests.constants
from app.tests.utils.files import FileWriter
from app.utils.security import hash_password
from app.db import db


class IntegrationUsers:

    @staticmethod
    def clear_users_table():
        db.execute("TRUNCATE TABLE USERS RESTART IDENTITY CASCADE;")


class UserGenerator:
    """
    Creates fake user information,
    very helpful for hashed passwords for example
    """

    def __init__(self):
        self._curr_user_id = 1
        self._email_ending = "@gmail.com"
        self._password = "password"

    def generate_fake_users_csv(self, num_users):
        FileWriter.write_csv_to_path(
            app.tests.constants.DEFAULT_FAKE_USER_CSV_OUTPUT,
            [[str(val) for key, val in user.items() if key != "password"] + ['', '', ''] for user in self.generate_users(num_users)]
        )

    def generate_fake_users_json(self, num_users):
        FileWriter.write_json_to_path(
            app.tests.constants.DEFAULT_FAKE_USER_JSON_OUTPUT,
            self.generate_users(num_users)
        )

    def generate_users(self, num_users):
        return [self.generate_next_user() for _ in range(num_users)]

    def generate_next_user(self):
        user = self.generate_user()
        self._curr_user_id += 1
        return user

    def generate_user(self):
        user = {
            'id': self.get_user_id(),
            "email": self.get_fake_email(),
            "hashed_password": self.get_fake_hashed_pw(),
            "password": self.get_fake_pw(),
        }
        return user

    def get_fake_email(self):
        return f"user{self.get_user_id()}{self.get_email_ending()}"

    def get_email_ending(self):
        return self._email_ending

    def get_user_id(self):
        return self._curr_user_id

    def get_fake_hashed_pw(self):
        return hash_password(self.get_fake_pw())

    def get_fake_pw(self):
        return self._password
