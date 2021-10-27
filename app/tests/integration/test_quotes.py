from copy import deepcopy 

from app.tests.client import client
from app.tests.utils.users import UserGenerator, create_users, get_auth_user_header
from app.tests.utils.algos import AlgoGenerator, create_algos
from app.tests.utils.shared import IntegrationClear
from app.tests.utils.quotes import get_intervals

class TestQuotes:

    @classmethod
    def setup_class(cls):
        cls.user_generator = UserGenerator()
        cls.mock_users = cls.user_generator.generate_users(2)
        cls.auth_user = cls.mock_users[0]

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self):
        IntegrationClear.clear_users_table()
        create_users(self.mock_users)

    def teardown_method(self):
        IntegrationClear.clear_users_table()
    
    def test_get_intervals(self):

        get_intervals(self.auth_user)

        