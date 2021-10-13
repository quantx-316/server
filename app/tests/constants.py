import os 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
DEFAULT_FAKE_USER_JSON_OUTPUT = os.path.join(DATA_DIR, 'auto_fake_users.json')
DEFAULT_FAKE_USER_CSV_OUTPUT = os.path.join(DATA_DIR, 'auto_fake_users.csv')