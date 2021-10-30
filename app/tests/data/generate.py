from app.tests.utils.users import UserGenerator
from app.tests.utils.algos import AlgoGenerator
from app.tests.utils.backtests import BacktestGenerator

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


if __name__ == "__main__":
    generate_user_csv_data(10)
