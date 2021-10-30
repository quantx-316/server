from copy import deepcopy
from datetime import datetime 
from app.tests.client import client
from app.tests.utils.users import UserGenerator, create_users, get_auth_user_header
from app.tests.utils.algos import AlgoGenerator, create_algos
from app.tests.utils.shared import IntegrationClear
from app.tests.utils.quotes import get_intervals 
from app.utils.time import datetime_to_unix
from app.tests.utils.backtests import create_backtest_test
import pprint 


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
    
    def test_delete_backtest(self):
        auth_header = get_auth_user_header(self.auth_user['email'], self.auth_user['password'])
        backtest = self.test_create_backtest()

        res = client.delete(
            "/backtest/" + "?backtest_id=" + str(backtest['id']),
            headers=auth_header,
        )
        print(res.status_code)
        assert res.status_code == 200 

        res = client.get(
            "/backtest/" + "?backtest_id=" + str(backtest['id']),
            headers=auth_header
        )
        assert res.status_code != 201  
    
    def test_get_user_backtests(self):
        results = self.test_create_backtests()

        pprint.pprint(results)

        ids = [result['id'] for result in results]

        auth_header = get_auth_user_header(self.auth_user['email'], self.auth_user['password'])
        res = client.get(
            "/backtest/",
            headers=auth_header,
        )
        data = res.json()
        assert res.status_code == 200
        for test in data['items']:
            assert test['id'] in ids 
    
    def test_create_backtests(self):
        results = []
        for _ in range(3):
            res = self.test_create_backtest()
            results.append(res)
        return results 

    def test_create_backtest(self):

        test_algo_info = self.created_algos[0]
        start, end = get_intervals(self.auth_user)
        start, end = datetime_to_unix(start), datetime_to_unix(end)

        return create_backtest_test(test_algo_info['id'], self.auth_user, start, end)
