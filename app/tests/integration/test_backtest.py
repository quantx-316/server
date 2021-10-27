from copy import deepcopy
from datetime import datetime 
from app.tests.client import client
from app.tests.utils.users import UserGenerator, create_users, get_auth_user_header
from app.tests.utils.algos import AlgoGenerator, create_algos
from app.tests.utils.shared import IntegrationClear
from app.tests.utils.quotes import get_intervals 
from app.utils.time import datetime_to_unix

class TestBacktests:

    @classmethod
    def setup_class(cls):
        cls.user_generator = UserGenerator()
        cls.mock_users = cls.user_generator.generate_users(2)
        cls.auth_user = cls.mock_users[0]
        cls.algo_generator = AlgoGenerator()
        cls.mock_algos = cls.algo_generator.generate_algos(3)

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self):
        IntegrationClear.clear_users_table()
        create_users(self.mock_users)
        IntegrationClear.clear_algos_table()
        self.created_algos = create_algos(self.mock_algos, self.auth_user)
        IntegrationClear.clear_backtest_table()

    def teardown_method(self):
        IntegrationClear.clear_users_table()
        IntegrationClear.clear_algos_table()
        IntegrationClear.clear_backtest_table()

    def test_create_backtest(self):

        test_algo_info = self.created_algos[0]

        self.create_backtest_test(test_algo_info['id'])


    def create_backtest_test(self, algo_id: int):

        auth_header = get_auth_user_header(self.auth_user['email'], self.auth_user['password'])
        
        test_start, test_end = get_intervals(self.auth_user)
        test_start, test_end = datetime_to_unix(test_start), datetime_to_unix(test_end)

        res = client.post(
            "/backtest/",
            json={
                "algo": algo_id,
                "test_interval": "1m",
                "test_start": test_start,
                "test_end": test_end
            },
            headers=auth_header,
        )
        assert res.status_code == 200 
        data = res.json()
        assert 'id' in data 

        res = client.get(
            "/backtest/" + str(data['id']),
            headers=auth_header
        )
        assert res.status_code == 200 
        retrieved_data = res.json()
        
        for key in data:
            assert key in retrieved_data 
            if key == "result":
                if data[key] is not None:
                    assert retrieved_data[key] is not None 
            else:
                assert retrieved_data[key] == data[key]
