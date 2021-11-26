import os 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
FAKE_COMP_DESC = os.path.join(DATA_DIR, 'fake_desc.txt')
DEFAULT_TEST_START = "2020-01-01 00:00:00"
DEFAULT_TEST_END = "2021-01-30 00:00:00"
DEFAULT_FAKE_USER_JSON_OUTPUT = os.path.join(DATA_DIR, 'auto_fake_users.json')
DEFAULT_FAKE_USER_CSV_OUTPUT = os.path.join(DATA_DIR, 'auto_fake_users.csv')
DEFAULT_FAKE_ALGO_CSV_OUTPUT = os.path.join(DATA_DIR, 'auto_fake_algos.csv')
DEFAULT_FAKE_BACK_CSV_OUTPUT = os.path.join(DATA_DIR, 'auto_fake_back.csv')
DEFAULT_FAKE_COMP_CSV_OUTPUT = os.path.join(DATA_DIR, 'auto_fake_comps.csv')
DEFAULT_FAKE_COMP_ENTRY_CSV_OUTPUT = os.path.join(DATA_DIR, 'auto_fake_comp_entry.csv')
DEFAULT_FAKE_BACKTEST_RESULT = os.path.join(DATA_DIR, 'test_backtest_result.json')
DEFAULT_FAKE_BACKTEST_ERR = os.path.join(DATA_DIR, 'test_backtest_error.json')

# Parameters for number of fake csv data to generate 
NUM_FAKE_USERS = 100
NUM_FAKE_ALGOS_PER_USER = 100
NUM_COMPS_PER_USER = 10 # comps first, then submit all backtests 
NUM_BACKTESTS_PER_ALGO = 10
