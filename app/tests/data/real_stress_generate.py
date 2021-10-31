from app.db import db 
from app.tests.utils.shared import IntegrationClear
from app.tests.constants import (
    DEFAULT_FAKE_USER_CSV_OUTPUT,
    DEFAULT_FAKE_ALGO_CSV_OUTPUT,
    DEFAULT_FAKE_BACK_CSV_OUTPUT,
    NUM_FAKE_USERS, 
    NUM_FAKE_ALGOS_PER_USER,
    NUM_BACKTESTS_PER_ALGO,
)
from app.tests.data.generate import (
    generate_user_csv_data,
    generate_algo_csv_data,
    generate_backtest_csv_data,
)

def generate_csv_data():
    fake_users = generate_user_csv_data(NUM_FAKE_USERS)
    fake_user_ids = [user['id'] for user in fake_users]
    fake_algos = generate_algo_csv_data(fake_user_ids, NUM_FAKE_ALGOS_PER_USER)
    # ^ {id, owner, title, code}
    fake_backtests = generate_backtest_csv_data(fake_algos, NUM_BACKTESTS_PER_ALGO)

def reset_db_to_stress():
    """
        This will reset all the DB tables except for Quotes/Stock.
        It will then insert large amounts of user data
    """
    IntegrationClear.clear_all_tables()

    conn = db.engine.raw_connection()

    try:
        with conn.cursor() as cur:
            with open(DEFAULT_FAKE_USER_CSV_OUTPUT) as user_data:
                cur.copy_expert("""
                    COPY Users ( username, email, hashed_password )
                    FROM STDIN WITH CSV
                """, user_data)
            with open(DEFAULT_FAKE_ALGO_CSV_OUTPUT) as algo_data:
                cur.copy_expert("""
                    COPY Algorithm ( owner, title, code )
                    FROM STDIN WITH CSV 
                """, algo_data)
            with open(DEFAULT_FAKE_BACK_CSV_OUTPUT) as back_data:
                cur.copy_expert("""
                    COPY Backtest ( algo, owner, result, score, code_snapshot, test_interval, test_start, test_end )
                    FROM STDIN WITH CSV 
                """, back_data)

    except Exception as e:
        conn.rollback()
        print("EXCEPTION")
        print(e)
        print(str(e))

    else:
        conn.commit()

    finally:
        conn.close() 

if __name__ == "__main__":
    # generate_csv_data()
    reset_db_to_stress()