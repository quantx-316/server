import os 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DEFAULT_FAKE_USER_JSON_OUTPUT = os.path.join(DATA_DIR, 'auto_fake_users.json')
DEFAULT_FAKE_USER_CSV_OUTPUT = os.path.join(DATA_DIR, 'auto_fake_users.csv')
DEFAULT_FAKE_ALGO_CSV_OUTPUT = os.path.join(DATA_DIR, 'auto_fake_algos.csv')
DEFAULT_FAKE_BACK_CSV_OUTPUT = os.path.join(DATA_DIR, 'auto_fake_back.csv')

# Parameters for number of fake csv data to generate 
NUM_FAKE_USERS = 100 
NUM_FAKE_ALGOS_PER_USER = 100
NUM_BACKTESTS_PER_ALGO = 1
