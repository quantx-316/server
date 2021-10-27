from datetime import datetime 

from app.tests.utils.users import get_auth_user_header
from app.tests.client import client

def get_intervals(user_info):

    auth_header = get_auth_user_header(user_info['email'], user_info['password'])
    
    res = client.get(
        "/quote/range/",
        headers=auth_header,
    )

    assert res.status_code == 200
    data = res.json()
    assert 'min_time' in data 
    assert 'max_time' in data 

    min_time = datetime.fromisoformat(data['min_time'])
    max_time = datetime.fromisoformat(data['max_time'])
    
    return min_time, max_time 
