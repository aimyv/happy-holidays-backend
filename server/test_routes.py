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

    def test_delete_user(self, api):
        res = api.delete('/users/2')
        assert res.status == '204 NO CONTENT'
