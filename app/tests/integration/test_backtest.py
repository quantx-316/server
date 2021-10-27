from copy import deepcopy 

from app.tests.client import client
from app.tests.utils.users import UserGenerator, create_users, get_auth_user_header
from app.tests.utils.algos import AlgoGenerator, create_algos
from app.tests.utils.shared import IntegrationClear


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
        create_algos(self.mock_algos, self.auth_user)
        IntegrationClear.clear_backtest_table()

    def teardown_method(self):
        IntegrationClear.clear_users_table()
        IntegrationClear.clear_algos_table()
        IntegrationClear.clear_backtest_table()
    
    

    def test_delete_algo(self):
        fetched_algos = self.test_get_algos() 
        to_delete = fetched_algos[0]
        to_delete_id = to_delete['id']
        user = self.mock_users[0]
        auth_header = get_auth_user_header(user['email'], user['password'])
        
        res = client.get(
            f"/algo/?algo_id={to_delete_id}",
            headers=auth_header,
        )
        assert res.status_code == 200 

        res = client.delete(
            f"/algo/?algo_id={to_delete_id}",
            headers=auth_header,
        )

        res = client.get(
            f"/algo/?algo_id={to_delete_id}",
            headers=auth_header,
        )
        assert res.status_code == 404 

    def test_fail_update_algo(self):

        fetched_algos = self.test_get_algos() 
        old_algo = fetched_algos[0]
        new_algo = deepcopy(old_algo)
        new_algo['id'] = 9000
        user = self.mock_users[0]
        auth_header = get_auth_user_header(user['email'], user['password'])

        res = client.put(
            "/algo/",
            json=new_algo,
            headers=auth_header, 
        )

        assert res.status_code == 404 
    
    def test_update_algo(self):

        fetched_algos = self.test_get_algos() 
        old_algo = fetched_algos[0]
        new_algo = deepcopy(old_algo)
        new_algo['title'] = 'FAKE TITLE'
        user = self.mock_users[0]
        auth_header = get_auth_user_header(user['email'], user['password'])

        res = client.put(
            "/algo/",
            json=new_algo,
            headers=auth_header, 
        )

        assert res.status_code == 200 

        data = res.json()
        assert 'id' in data 
        assert data['id'] == old_algo['id']

        res = client.get(
            f"/algo/?algo_id={old_algo['id']}",
            headers=auth_header,
        )
        assert res.status_code == 200 
        data = res.json() 
        assert data['title'] == 'FAKE TITLE'
    
    def test_get_algos(self):
        orig_algos = self.test_create_algos()
        fetched_algos = self.get_algos_test() 
        assert len(orig_algos) == len(fetched_algos)
        orig_algo_mapping = {algo['id'] : algo for algo in orig_algos}
        for fetched_algo in fetched_algos:
            fetched_id = fetched_algo['id']
            assert fetched_id in orig_algo_mapping 
            orig_algo_obj = orig_algo_mapping[fetched_id]
            for attr in fetched_algo:
                assert attr in orig_algo_obj 
                assert fetched_algo[attr] == orig_algo_obj[attr]
        return fetched_algos 

    def get_algos_test(self):
        user = self.mock_users[0]
        auth_header = get_auth_user_header(user['email'], user['password'])
    
        res = client.get(
            "/algo/all/",
            headers=auth_header,
        )

        assert res.status_code == 200 
        return res.json() 

    def test_create_algos(self):
        algos = []
        for mock_algo in self.mock_algos:
            res = self.create_algo_test(mock_algo)
            algos.append(res)
        return algos 
    
    def test_create_algo(self):

        test_algo_info = self.mock_algos[0]

        self.create_algo_test(test_algo_info)


    def create_backtest_test(self, algo_id: int):

        auth_header = get_auth_user_header(self.auth_user['email'], self.auth_user['password'])
        
        res = client.post(
            "/backtest/",
            json={
                "algo": algo_id,
                "test_interval": "",
                "test_start": "",
                "test_end": ""
            }
        )


    def create_algo_test(self, algo_info: dict):

        user = self.mock_users[0]
        auth_header = get_auth_user_header(user['email'], user['password'])

        res = client.post(
            '/algo/',
            json=algo_info,
            headers=auth_header,
        )

        assert res.status_code == 200

        data = res.json() 
        algo_id = data['id']

        res = client.get(
            f"/algo/?algo_id={algo_id}",
            headers=auth_header,
        )
        assert res.status_code == 200 
        comp_data = res.json()
        assert comp_data['id'] == algo_id 
        assert comp_data['owner'] == data['owner']
        assert comp_data['code'] == data['code']
        assert comp_data['title'] == data['title']

        return comp_data 