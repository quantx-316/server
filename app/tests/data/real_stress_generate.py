from app.db import db 
from app.tests.utils.shared import IntegrationClear
from app.tests.constants import (
    DEFAULT_FAKE_COMP_CSV_OUTPUT,
    DEFAULT_FAKE_COMP_ENTRY_CSV_OUTPUT,
    DEFAULT_FAKE_USER_CSV_OUTPUT,
    DEFAULT_FAKE_ALGO_CSV_OUTPUT,
    DEFAULT_FAKE_BACK_CSV_OUTPUT,
    NUM_FAKE_USERS, 
    NUM_FAKE_ALGOS_PER_USER,
    NUM_BACKTESTS_PER_ALGO,
    NUM_COMPS_PER_USER,
)
from app.tests.data.generate import (
    generate_user_csv_data,
    generate_algo_csv_data,
    generate_backtest_csv_data,
    generate_comp_csv_data,
    generate_comp_entry_csv_data,
)
from time import time 

def generate_csv_data():

    print()

    print("Beginning fake user generation")
    fake_users = generate_user_csv_data(NUM_FAKE_USERS)
    print("Finished generating fake user csv data")
    print("Beginning fake comp generation")
    fake_comps = generate_comp_csv_data(fake_users, NUM_COMPS_PER_USER)
    print("Finished generating fake comp csv data")

    fake_user_ids = [user['id'] for user in fake_users]
    print("Beginning fake algo generation")
    fake_algos = generate_algo_csv_data(fake_user_ids, NUM_FAKE_ALGOS_PER_USER)
    print("Finished generating fake algo csv data")
    # ^ {id, owner, title, code}
    print("Beginning fake backtest generation")
    fake_backtests = generate_backtest_csv_data(fake_algos, NUM_BACKTESTS_PER_ALGO)
    print("Finished generating fake backtest csv data")
    print("Beginning fake comp entry generation")
    fake_entries = generate_comp_entry_csv_data(fake_comps, fake_backtests, fake_users)
    print("Finished generating fake comp entry csv data")

    print("FINISHED GENERATION")

    print()

def reset_db_to_stress():
    """
        This will reset all the DB tables except for Quotes/Stock.
        It will then insert large amounts of user data
    """
    print()
    print("CLEARING ALL DB TABLES (except Quotes/Stock)")
    IntegrationClear.clear_all_tables()
    print("FINISHED CLEARING ALL DB TABLES (except Quotes/Stock)")

    conn = db.engine.raw_connection()
    print()
    print("BEGINNING TO COPY DATA --- WAIT FOR COMMIT AND CLOSING")

    try:
        with conn.cursor() as cur:
            print("COPYING USER DATA INTO TABLE")
            with open(DEFAULT_FAKE_USER_CSV_OUTPUT) as user_data:
                cur.copy_expert("""
                    COPY Users ( username, email, hashed_password )
                    FROM STDIN WITH CSV
                """, user_data)
            print("FINISHED COPYING")
            print("COPYING COMP DATA INTO TABLE")
            with open(DEFAULT_FAKE_COMP_CSV_OUTPUT) as comp_data: 
                cur.copy_expert("""
                    COPY Competition ( title, description, owner, end_time, test_start, test_end )
                    FROM STDIN WITH CSV 
                """, comp_data)
            print("FINISHED COPYING")
            print("COPYING ALGO DATA INTO TABLE")
            with open(DEFAULT_FAKE_ALGO_CSV_OUTPUT) as algo_data:
                cur.copy_expert("""
                    COPY Algorithm ( owner, title, code, public )
                    FROM STDIN WITH CSV 
                """, algo_data)
            print("FINISHED COPYING")
            print("COPYING BACKTEST DATA INTO TABLE")
            with open(DEFAULT_FAKE_BACK_CSV_OUTPUT) as back_data:
                cur.copy_expert("""
                    COPY Backtest ( algo, owner, result, score, code_snapshot, test_interval, test_start, test_end )
                    FROM STDIN WITH CSV 
                """, back_data)
            print("FINISHED COPYING")
            print("COPYING COMP ENTRY DATA INTO TABLE")
            with open(DEFAULT_FAKE_COMP_ENTRY_CSV_OUTPUT) as comp_entry_data:
                cur.copy_expert("""
                    COPY CompetitionEntry ( comp_id, owner, backtest_id, backtest_algo, result, score, code_snapshot, test_interval, test_start, test_end )
                    FROM STDIN WITH CSV
                """, comp_entry_data)
            print("FINISHED COPYING")

        print("FINISHED COPYING --- WAIT FOR COMMIT AND CLOSING")
        print()


    except Exception as e:
        conn.rollback()
        print("EXCEPTION")
        print(e)
        print(str(e))

    else:
        print("COMMITTING CHANGES")
        conn.commit()
        print("FINISHED COMMITTING")

    finally:
        print("CLOSING CONNECTION")
        conn.close()
        print("CONNECTION CLOSED")

if __name__ == "__main__":
    # generate_csv_data()
    reset_db_to_stress()