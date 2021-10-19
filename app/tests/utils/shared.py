from app.db import db

class IntegrationClear:

    @staticmethod 
    def truncate_table(table_name: str):
        db.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;")

    @staticmethod
    def clear_algos_table():
        IntegrationClear.truncate_table("ALGORITHM")
    
    @staticmethod
    def clear_users_table():
        IntegrationClear.truncate_table("USERS")
