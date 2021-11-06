from app.tests.utils.users import UserGenerator
from app.tests.utils.algos import AlgoGenerator
from app.tests.utils.backtests import BacktestGenerator
import json
import random

def generate_backtest_csv_data(fake_algos, num_backtests):
    generator = BacktestGenerator()
    return generator.generate_csv_user_backtests(fake_algos, num_backtests)

def generate_algo_csv_data(user_ids, num_algos):
    generator = AlgoGenerator()
    return generator.generate_csv_user_algos(user_ids, num_algos)

def generate_user_csv_data(num_users):
    generator = UserGenerator()
    return generator.generate_fake_users_csv(num_users)


def generate_user_json_data(num_users):
    generator = UserGenerator()
    generator.generate_fake_users_json(num_users)


def generate_test_backtest_result():

    with open('test_backtest_result.json') as f:
        res = json.load(f)

    new_json = []

    for first_min in range(1, 6):
        for second_min in range(10):
            obj = {
                "time": f"2020-01-02 14:{first_min}{second_min}:00",
                "portfolio": {
                    "value": first_min * (second_min+1) * 100,
                    "positions": [
                        {
                            "symbol": "AAPL",
                            "num_shares": 1,
                            "price": 75.0
                        },
                    ],
                    "cash": first_min * (second_min+1) * 50,
                    "errors": [
                        {
                            "description": "(exception name etc)"
                        }
                    ]
                }
            }
            new_json.append(obj)

    res['portfolio_over_time'] = new_json
    res['roi'] = random.randint(0, 100)


    with open('test_backtest_result.json', 'r+') as f:
        f.truncate(0)
        f.write(json.dumps(res, indent=4))

if __name__ == "__main__":
    # generate_user_csv_data(10)
    generate_test_backtest_result()
