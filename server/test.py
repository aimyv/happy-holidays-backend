import json


class TestAPICase():
    def test_home(self, api):
        resp = api.get('/')
        assert resp.status == '200 OK'
        assert res.json['message'] == 'Hello, from Flask!'
