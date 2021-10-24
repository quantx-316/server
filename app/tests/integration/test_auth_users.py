from app.tests.client import client
from app.tests.utils.users import UserGenerator, auth_user_test, create_user
from app.tests.utils.shared import IntegrationClear

class TestAuthUsers:

    @classmethod
    def setup_class(cls):
        cls.user_generator = UserGenerator()
        cls.mock_users = cls.user_generator.generate_users(10)

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self):
        IntegrationClear.clear_users_table()

    def teardown_method(self):
        IntegrationClear.clear_users_table()

    # test invalid update (try to change to email already existing)
    def test_invalid_update_user(self):
        """
        Tests for invalid update if trying to 
        update with a unique key 
        """
        self.test_create_users()
        mock_user = self.mock_users[0]
        creds = auth_user_test(mock_user['email'], mock_user['password'])
        access_token = creds['access_token']
        auth_header = {"Authorization":  f"Bearer {access_token}"}

        copy_user = mock_user.copy()
        del copy_user['password']
        del copy_user['hashed_password']
        del copy_user['id']
        old_user = copy_user.copy() 
        new_user = copy_user.copy() 
        firstname, lastname = "John", "Doe"
        new_user['email'] = self.mock_users[1]['email']
        new_user['firstname'] = firstname
        new_user['lastname'] = lastname 
        try:
            res = client.put(
                '/user/',
                json={
                    'old_user': old_user,
                    'new_user': new_user,
                },
                headers=auth_header,
            )
            assert False == True # reach this point, shouldve thrown exception above 
        except Exception as e: 
            print(e)

    def test_update_user(self):
        """
        Tests for successful authentication and update 
        of user 
        """
        self.test_create_users()
        mock_user = self.mock_users[0]
        creds = auth_user_test(mock_user['email'], mock_user['password'])
        access_token = creds['access_token']
        auth_header = {"Authorization":  f"Bearer {access_token}"}
        

        copy_user = mock_user.copy()
        del copy_user['password']
        del copy_user['hashed_password']
        user_id = copy_user['id']
        old_user = copy_user.copy() 
        new_user = copy_user.copy() 
        firstname, lastname = "John", "Doe"
        new_user['email'] = 'randemail@gmail.com'
        new_user['firstname'] = firstname
        new_user['lastname'] = lastname 


        res = client.put(
            '/user/',
            json={
                'old_user': old_user,
                'new_user': new_user,
            },
            headers=auth_header,
        )
        assert res.status_code == 200
        data = res.json() 
        assert data['id'] == user_id 
        assert data['email'] == new_user['email']
        assert data['firstname'] == new_user['firstname']
        assert data['lastname'] == new_user['lastname']

    
    def test_get_current_user(self):
        """
        Tests for successful authentication and retrieval of
        current user 
        """
        self.test_create_users()
        mock_user = self.mock_users[0]
        creds = auth_user_test(mock_user['email'], mock_user['password'])
        access_token = creds['access_token']
        auth_header = {"Authorization":  f"Bearer {access_token}"}
        res = client.get(
            '/user/current/',
            headers=auth_header,
        )
        assert res.status_code == 200 
        data = res.json() 
        assert 'email' in data
        assert 'id' in data 
        assert data['email'] == mock_user['email']
        assert data['id'] == mock_user['id']
    
    def test_fail_get_current_user(self):
        """
        Tests for failure to authenticate current user endpt
        """
        res = client.get(
            'users/current/',
        )
        assert res.status_code != 200 
        assert res.status_code != 500

    def test_successful_auth_users(self):
        """
        Tests for successful accessing secured users endpoint
        """
        self.test_create_users()
        mock_user = self.mock_users[0]
        creds = auth_user_test(mock_user['email'], mock_user['password'])
        res = self.access_users_endpt(creds=creds)
        assert res.status_code == 200
        data = res.json()
        id_to_email = {}
        for user in self.mock_users:
            id_to_email[user['id']] = user['email']
        for user in data:
            assert 'email' in user 
            assert 'id' in user 
            assert 'firstname' in user 
            assert 'lastname' in user 
            assert 'email' in user 
            assert 'hashed_password' not in user 
            assert 'password' not in user 
            user_email, user_id = user['email'], user['id']
            assert user_id in id_to_email 
            assert user_email == id_to_email[user_id]

    def test_fail_auth_users(self):
        """
        Tests for failing to access secured users endpoint
        """
        res = self.access_users_endpt()
        assert res.status_code != 200
        assert res.status_code != 500

    def access_users_endpt(self, creds=None):
        if creds:
            res = client.get(
                '/user/all/',
                headers={'Authorization': f'Bearer {creds["access_token"]}'}
            )
        else:
            res = client.get(
                '/user/all/'
            )
        return res

    def test_auth_users(self):
        """
        Tests for successful token retrieval for 10 authenticated
        mock users
        """
        self.test_create_users()
        for mock_user in self.mock_users:
            auth_user_test(mock_user['email'], mock_user['password'])

    def test_create_users(self):
        """
        Tests successful creation (and retrieval) of 10 mock users
        """
        for mock_user in self.mock_users:
            self.create_user_test(mock_user)
            
    def create_user_test(self, user_info: dict):
        """
        Tests POST /user/, GET /user/user_id, GET /user/user_email
        """
        data = create_user(user_info)

        token = auth_user_test(user_info['email'], user_info['password'])
        access_token = token['access_token']

        auth_header = {"Authorization":  f"Bearer {access_token}"}

        user_id = data["id"]
        res = client.get(
            f"/user/?user_id={user_id}",
            headers=auth_header,
        )
        assert res.status_code == 200
        data = res.json()
        assert data["email"] == user_info['email']
        assert data["id"] == user_id

        user_email = data['email']
        res = client.get(
            f"/user/?user_email={user_email}",
            headers=auth_header, 
        )
        assert res.status_code == 200 
        data = res.json() 
        assert data['email'] == user_info['email']
        assert data['id'] == user_id 