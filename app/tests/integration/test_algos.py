from app.tests.client import client
from app.tests.utils.users import UserGenerator, create_users, get_auth_user_header
from app.tests.utils.shared import IntegrationClear

class TestAlgos:

    @classmethod
    def setup_class(cls):
        cls.user_generator = UserGenerator()
        cls.mock_users = cls.user_generator.generate_users(2)

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self):
        IntegrationClear.clear_users_table()
        create_users(self.mock_users)
        IntegrationClear.clear_algos_table()

    def teardown_method(self):
        IntegrationClear.clear_algos_table()
    
    def test_create_algo(self):

        test_algo_info = {
            "title": "test algo",
            "code": "def randCode(): pass"
        }

        self.create_algo_test(test_algo_info)

    def create_algo_test(self, algo_info: dict):

        user = self.mock_users[0]
        auth_header = get_auth_user_header(user['email'], user['password'])

        res = client.post(
            '/algo/',
            json=algo_info,
            headers=auth_header,
        )

        print(res.status_code)


# class AlgoBase(BaseModel):
#     title: str 
#     code: str 

# class AlgoSubmit(AlgoBase):
#     pass 

# class AlgoDB(AlgoBase):
#     id: int 
#     owner: int 
#     created: datetime 
#     edited_at: datetime 

#     class Config: 
#         orm_mode = True 
