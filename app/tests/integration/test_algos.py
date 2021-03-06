from copy import deepcopy 

from app.tests.client import client
from app.tests.utils.users import UserGenerator, create_users, get_auth_user_header
from app.tests.utils.algos import AlgoGenerator, create_algo_test, create_algos
from app.tests.utils.shared import IntegrationClear

import pprint 


class TestAlgos:

    @classmethod
    def setup_class(cls):
        cls.user_generator = UserGenerator()
        cls.mock_users = cls.user_generator.generate_users(2)
        cls.algo_generator = AlgoGenerator()
        cls.mock_algos = cls.algo_generator.generate_algos(3)

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self):
        IntegrationClear.clear_users_table()
        create_users(self.mock_users)
        IntegrationClear.clear_algos_table()

    def teardown_method(self):
        IntegrationClear.clear_users_table()
        IntegrationClear.clear_algos_table()
    
    # TODO: (not necessarily required)
        # need failed create, failed update (diff user than owner), failed delete (diff user)
        # failed getting of algos for a user if diff user, or have no creds
            # can do fail because of no creds all at once 

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

        pprint.pprint(orig_algos)
        pprint.pprint(fetched_algos)

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
        return res.json()['items']

    def test_create_algos(self):
        return create_algos(self.mock_algos, self.mock_users[0])
    
    def test_create_algo(self):

        test_algo_info = self.mock_algos[0]

        create_algo_test(test_algo_info, self.mock_users[0])
