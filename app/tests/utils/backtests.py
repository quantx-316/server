from app.tests.client import client
from app.tests.utils.users import  get_auth_user_header
from app.tests.utils.files import FileWriter
import app.tests.constants
import random
import json

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
        self.test_start = app.tests.constants.DEFAULT_TEST_START
        self.test_end = app.tests.constants.DEFAULT_TEST_END
        self.test_interval = "1m"

    def generate_csv_user_backtests(self, fake_algos, num_backtests):

        csv_info = [] 
        ret = []

        with open(app.tests.constants.DEFAULT_FAKE_BACKTEST_RESULT) as f:
            test_result = json.load(f)
            test_str_res = json.dumps(test_result, indent=4)

        with open(app.tests.constants.DEFAULT_FAKE_BACKTEST_ERR) as f:
            test_error = json.load(f)
            test_str_err = json.dumps(test_error, indent=4)

        for algo in fake_algos:
            first_half = num_backtests // 2
            second_half = num_backtests - first_half
            for _ in range(first_half):
                score = random.randint(0, 100)
                csv_info.append([
                    str(algo['id']),
                    str(algo['owner']),
                    test_str_res,
                    str(score),
                    str(algo['code']),
                    self.test_interval, 
                    str(self.test_start),
                    str(self.test_end),
                ])
                ret.append({
                    "id": self._curr_backtest_id,
                    "algo": algo['id'],
                    "owner": algo['owner'], 
                    "code": str(algo['code']),
                    "result": test_str_res,
                    "score": score,
                    "test_interval": self.test_interval, 
                    "test_start": self.test_start, 
                    "test_end": self.test_end, 
                })
                self._curr_backtest_id += 1

            for _ in range(second_half):
                csv_info.append([
                    str(algo['id']),
                    str(algo['owner']),
                    test_str_err,
                    str(-1),
                    str(algo['code']),
                    self.test_interval,
                    str(self.test_start),
                    str(self.test_end),
                ])
                ret.append({
                    "id": self._curr_backtest_id,
                    "algo": algo['id'],
                    "code": str(algo['code']),
                    "owner": algo['owner'],
                    "result": test_str_err,
                    "score": -1,
                    "test_interval": self.test_interval,
                    "test_start": self.test_start,
                    "test_end": self.test_end,
                })
                self._curr_backtest_id += 1

        FileWriter.write_csv_to_path(
            app.tests.constants.DEFAULT_FAKE_BACK_CSV_OUTPUT,
            csv_info 
        )

        return ret 
