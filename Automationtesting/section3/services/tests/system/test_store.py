import json
from basetest import BaseTest

class TestStore(BaseTest):
    def setUp(self):
        super().setUp()
        with self.app() as client:
            res = client.post('/login',json={"username":"oman","password":"asdasd"})
            token = json.loads(res.data)['access_token']
            self.token = f"Bearer {token}"

    def test_a_store_name(self):
        with self.app() as client:
            res = client.post('/store/unittest',headers={"Authorization":self.token})
            self.assertEqual(res.status_code, 201)

    def test_b_get_store(self):
        with self.app() as client:
            res = client.get('/store/unittest')
            self.assertEqual(res.status_code,200)

    def test_c_get_all_data(self):
        with self.app() as client:
            res = client.get('/stores',headers={"Authorization":self.token})
            self.assertEqual(res.status_code,200)

    def test_d_delete_store(self):
        with self.app() as client:
            res = client.delete('/store/unittest',headers={"Authorization":self.token})
            self.assertEqual(res.status_code, 200)
