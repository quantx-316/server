from app.tests.client import client
from app.tests.utils.users import  get_auth_user_header
from app.tests.utils.files import FileWriter
import app.tests.constants
import random

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

    # res = client.get(
    #     "/backtest/" + "?backtest_id=" + str(data['id']),
    #     headers=auth_header
    # )
    # assert res.status_code == 200 
    # retrieved_data = res.json()

    return data


class BacktestGenerator:
    """
    Creates fake backtest information
    """

    # owner, title, code
    def __init__(
        self,
    ):
        self._curr_backtest_id = 1 
        self.test_start = "2018-12-17 09:31:00"
        self.test_end = "2021-02-12 14:51:00" 
        self.test_interval = "1m"
        self.result="{message: 'test'}"
        self.score=50

    def generate_csv_user_backtests(self, fake_algos, num_backtests):

        csv_info = [] 
        ret = []
        for algo in fake_algos:
            for _ in range(num_backtests):
                score = random.randint(0,100)
                csv_info.append([
                    str(algo['id']),
                    str(algo['owner']),
                    self.result,
                    str(score),
                    str(algo['code']),
                    self.test_interval, 
                    str(self.test_start),
                    str(self.test_end),
                ])
                ret.append({
                    "algo": algo['id'],
                    "owner": algo['owner'], 
                    "result": self.result, 
                    "score": score,
                    "test_interval": self.test_interval, 
                    "test_start": self.test_start, 
                    "test_end": self.test_end, 
                })

        FileWriter.write_csv_to_path(
            app.tests.constants.DEFAULT_FAKE_BACK_CSV_OUTPUT,
            csv_info 
        )

        return ret 
