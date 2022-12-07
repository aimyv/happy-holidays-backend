import json


class TestAPICase():
    def test_home(self, api):
        res = api.get('/')
        assert res.status == '200 OK'
        assert res.json['message'] == 'Hello, from Flask!'

    def test_register(self, api):
        mock_data = json.dumps({
            "email": "test@test.com",
            "username": "test",
            "password1": "123",
            "password2": "123"
        })
        mock_headers = {'Content-Type': 'application/json'}
        res = api.post('/register', data=mock_data, headers=mock_headers)
        assert res.status == '201 CREATED'
        assert res.json['message'] == 'User created!'

    def test_existing_email(self, api):
        mock_data = json.dumps({
            "email": "test@test.com",
            "username": "test",
            "password1": "123",
            "password2": "123"
        })
        mock_headers = {'Content-Type': 'application/json'}
        res = api.post('/register', data=mock_data, headers=mock_headers)
        assert res.status == '400 BAD REQUEST'

    def test_existing_username(self, api):
        mock_data = json.dumps({
            "email": "test1@test.com",
            "username": "test",
            "password1": "123",
            "password2": "123"
        })
        mock_headers = {'Content-Type': 'application/json'}
        res = api.post('/register', data=mock_data, headers=mock_headers)
        assert res.status == '400 BAD REQUEST'

    def test_mismatched_passwords(self, api):
        mock_data = json.dumps({
            "email": "test1@test.com",
            "username": "test",
            "password1": "12",
            "password2": "123"
        })
        mock_headers = {'Content-Type': 'application/json'}
        res = api.post('/register', data=mock_data, headers=mock_headers)
        assert res.status == '400 BAD REQUEST'

    def test_login(self, api):
        mock_data = json.dumps({
            "email": "test@test.com",
            "password": "123"
        })
        mock_headers = {'Content-Type': 'application/json'}
        res = api.post('/login', data=mock_data, headers=mock_headers)
        assert res.status == '201 CREATED'
        assert res.json['username'] == "test"
        assert res.json['message'] == "Logged In."

    def test_login_incorrect_email(self, api):
        mock_data = json.dumps({
            "email": "test1@test.com",
            "password": "123"
        })
        mock_headers = {'Content-Type': 'application/json'}
        res = api.post('/login', data=mock_data, headers=mock_headers)
        assert res.status == '404 NOT FOUND'

    def test_login_incorrect_password(self, api):
        mock_data = json.dumps({
            "email": "test@test.com",
            "password": "12"
        })
        mock_headers = {'Content-Type': 'application/json'}
        res = api.post('/login', data=mock_data, headers=mock_headers)
        assert res.status == '400 BAD REQUEST'

    def test_get_all_users(self, api):
        res = api.get('/users')
        assert res.status == '200 OK'

    def test_get_specific_user(self, api):
        test = api.get('/users/test')
        assert test.status == '200 OK'

    def test_get_nonexistant_user(self, api):
        test = api.get('/users/test1')
        assert test.status == '400 BAD REQUEST'
        res = api.get('/users/-1')
        assert test.status == '400 BAD REQUEST'

    def test_get_friends(self, api):
        test = api.get('/users/test')
        assert test.status == '200 OK'
        user_id = test.json["id"]
        res = api.get(f'/users/{user_id}/friends')
        assert test.status == '200 OK'

    def test_add_friend(self, api):
        test = api.get('/users/test')
        user_id = test.json["id"]
        mock_data = json.dumps({
            "email": "test2@test2.com",
            "username": "test2",
            "password1": "123",
            "password2": "123"
        })
        mock_headers = {'Content-Type': 'application/json'}
        res = api.post('/register', data=mock_data, headers=mock_headers)
        mock_data = json.dumps({
            "friend": "test2",
        })
        res = api.post(f'/users/{user_id}/friends',
                       data=mock_data, headers=mock_headers)
        assert res.status == '201 CREATED'
        res = api.get(f'/users/{user_id}/friends')
        assert len(res.json) == 1

    def test_logout(self, api):
        res = api.get('/logout')
        assert res.status == '200 OK'

    def test_delete_user(self, api):
        res = api.delete('/users/test')
        assert res.status == '204 NO CONTENT'
        res = api.delete('/users/test2')
        assert res.status == '204 NO CONTENT'