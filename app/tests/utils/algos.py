from app.tests.client import client
from app.tests.utils.users import get_auth_user_header
from app.tests.utils.files import FileWriter
import app.tests.constants

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

def create_algo(algo_info: dict, user: dict):
    auth_header = get_auth_user_header(user['email'], user['password'])

    res = client.post(
        '/algo/',
        json=algo_info,
        headers=auth_header,
    )

    assert res.status_code == 200

    data = res.json() 

    return data 

def create_algos_lite(algo_infos, user: dict):
    algos = []
    for algo_info in algo_infos:
        res = create_algo(algo_info, user)
        algos.append(res)
    return algos 

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

    # owner, title, code
    def __init__(self):
        self._curr_algo_id = 1 

    def generate_csv_user_algos(self, user_ids, num_algos):

        ret = [] 

        info = [] 
        for user_id in user_ids:
            fake_algos = self.generate_realistic_fake_algos(num_algos)
            for algo in fake_algos:
                ret.append({
                    "id": algo['id'],
                    "owner": user_id,
                    "title": algo['title'],
                    "code": algo['code']
                })
                info.append([
                    str(user_id),
                    str(algo['title']),
                    str(algo['code'])
                ])
    
        FileWriter.write_csv_to_path(
            app.tests.constants.DEFAULT_FAKE_ALGO_CSV_OUTPUT,
            info
        )

        return ret 
    
    def generate_realistic_fake_algos(self, num_algos):
        return [self.generate_realistic_fake_algo() for _ in range(num_algos)]
    
    def generate_realistic_fake_algo(self):
        info = {
            "id": self._curr_algo_id,
            "title": "test algo",
            "code": "def randCode(): pass"
        }
        self._curr_algo_id += 1
    
        return info 

    def generate_algos(self, num_algos = 1):
        return [self.get_fake_algo() for _ in range(num_algos)]
    
    def get_fake_algo(self):
        return {
            "title": "test algo",
            "code": "def randCode(): pass"
        }
