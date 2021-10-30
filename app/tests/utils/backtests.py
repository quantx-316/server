from app.tests.client import client
from app.tests.utils.users import  get_auth_user_header

def create_backtest_test(
    algo_id: int, 
    user_info: dict,
    test_start, 
    test_end,
):

    auth_header = get_auth_user_header(user_info['email'], user_info['password'])

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
        "/backtest/" + "?backtest_id=" + str(data['id']),
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

    return retrieved_data 
