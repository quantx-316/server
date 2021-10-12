from app.tests.utils.users import UserGenerator


def generate_user_csv_data(num_users):
    generator = UserGenerator()
    generator.generate_fake_users_csv(num_users)


def generate_user_json_data(num_users):
    generator = UserGenerator()
    generator.generate_fake_users_json(num_users)


if __name__ == "__main__":
    generate_user_csv_data(10)
