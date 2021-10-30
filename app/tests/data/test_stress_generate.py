from sqlalchemy.sql.functions import user
from app.tests.utils.users import UserGenerator, create_users, get_auth_user_header
from app.tests.utils.algos import AlgoGenerator, create_algos_lite
from app.tests.utils.backtests import create_backtest_test
from app.tests.utils.quotes import get_intervals 
from app.utils.time import unix_to_utc_datetime
from app.tests.utils.shared import IntegrationClear

# ADJUST THESE FOR STRESS GENERATION
NUM_USERS = 100 
NUM_ALGOS_PER_USER = 100 
BACKTESTS_PER_ALGO = 1 # there will be 10,000 algorithms with 100x100

def generate_backtests(
    min_, max_,
    user_to_algo,
):

    for user_id in user_to_algo:
        algos = user_to_algo[user_id]['algos']
        user_info = user_to_algo[user_id]['user_obj']
        create_backtest_test(algos['id'], user_info, min_, max_)


def generate_algos(users):
    mock_algos = AlgoGenerator().generate_algos(NUM_ALGOS_PER_USER)
    user_to_algo = {}
    for user in users:
        algos = create_algos_lite(mock_algos, user)
        user_to_algo[user['id']] = {
            'user_obj': user,
            'algos': algos,
        }
    return user_to_algo 

def generate_users():
    mock_users = UserGenerator().generate_users(NUM_USERS)
    users = create_users(mock_users)
    return (users, mock_users)  

def generate_stress_data():

    # CLEAR TABLES FIRST 
    IntegrationClear.clear_all_tables()

    # GENERATE USERS
    users, mock_users = generate_users() 

    # GENERATE ALGORITHMS 
    user_to_algo = generate_algos(mock_users)

    min_, max_ = get_intervals(mock_users[0])
    min_, max_ = unix_to_utc_datetime(min_), unix_to_utc_datetime(max_)

    # GENERATE BACKTESTS WITH MAX INTERVALS
    generate_backtests(min_, max_, user_to_algo)

    # GENERATE COMPETITIONS 


class TestStress:

    @classmethod
    def setup_class(cls):
        generate_stress_data()
    
    def test_placeholder(self):
        pass 
