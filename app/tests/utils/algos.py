from app.tests.client import client
from app.tests.utils.users import get_auth_user_header

def create_algo_test(algo_info: dict, user: dict):

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

def create_algos(algo_infos, user: dict):
    algos = []
    for algo_info in algo_infos:
        res = create_algo_test(algo_info, user) 
        algos.append(res)
    return algos 

class AlgoGenerator:
    """
    Creates fake algo information
    """

    def generate_algos(self, num_algos = 1):
        return [self.get_fake_algo() for _ in range(num_algos)]
    
    def get_fake_algo(self):
        return {
            "title": "test algo",
            "code": "def randCode(): pass"
        }
