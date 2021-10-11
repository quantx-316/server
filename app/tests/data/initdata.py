import os

from app.db import get_db
from app.models.users import Users
from app.tests import constants
from app.tests.data import generate
from app.tests.utils.files import FileReader


def init_user_data(num_users=10):
    if not os.path.exists(constants.DEFAULT_FAKE_USER_JSON_OUTPUT):
        generate.generate_user_json_data(num_users)
    users = FileReader.read_json_from_path(constants.DEFAULT_FAKE_USER_JSON_OUTPUT)
    for user in users:
        Users.create_user(get_db(), )


if __name__ == "__main__":
    init_user_data()
