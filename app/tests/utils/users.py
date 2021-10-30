from typing import List 

import app.tests.constants
from app.tests.client import client
from app.tests.utils.files import FileWriter
from app.utils.security import hash_password
from app.db import db


def create_user(user_info: dict):
    res = client.post(
        '/user/',
        json={
            "email": user_info['email'], 
            "username": user_info['username'],
            "password": user_info['password'], 
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert data["email"] == user_info['email']
    assert "id" in data
    return data 


def create_users(user_infos: List[dict]): 
    all_info = []
    for user_info in user_infos:
        user_data = create_user(user_info)
        all_info.append(user_data)
    return all_info 


def auth_user_test(username, password):
    res = client.post(
        '/token',
        data={"username": username, "password": password}
    )
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert "user" in data 
    user_data = data['user']
    assert "username" in user_data 
    assert user_data['email'] == username 
    return data


def get_auth_user_token(username, password):
    creds = auth_user_test(username, password)
    return creds['access_token']


def get_auth_user_header(username, password):
    access_token = get_auth_user_token(username, password)
    return {"Authorization": f"Bearer {access_token}"}


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
            [[str(val) for key, val in user.items() if key != "password"] for user in self.generate_users(num_users)]
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
            "username": self.get_username(),
            "email": self.get_fake_email(),
            "hashed_password": self.get_fake_hashed_pw(),
            "password": self.get_fake_pw(),
            "firstname": None, 
            "lastname": None, 
            "description": None, 
        }
        return user
    
    def get_username(self):
        return f"user{self.get_user_id()}"

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
