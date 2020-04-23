import json
from basetest import BaseTest
from services.models.UserModel import UserModel

class UserTest(BaseTest):
    def test_a_register_user(self):
        with self.app() as client:
            res = client.post('/register',json={"username":"test1","password":"asdasd"})
            self.assertEqual(res.status_code, 201)
            self.assertIsNotNone(UserModel.query.filter_by(username='test1').first())

    def test_b_login_user(self):
        with self.app() as client:
            res = client.post('/login',json={"username":"test1","password":"asdasd"})
            self.assertIn('access_token',json.loads(res.data).keys())

    def test_c_check_duplicate_account(self):
        with self.app() as client:
            res = client.post('/register',json={"username":"test1","password":"asdasd"})
            self.assertEqual(res.status_code, 400)
            self.assertDictEqual(json.loads(res.data),{'username': ['Username cannot be duplicated']})

    def test_d_check_len_password(self):
        with self.app() as client:
            res = client.post('/register',json={"username":"test1","password":"asd"})
            self.assertDictEqual(json.loads(res.data),{'password': ['Shorter than minimum length 6.']})
            res2 = client.post('/login',json={"username":"test1","password":"asd"})
            self.assertDictEqual(json.loads(res2.data),{'password': ['Shorter than minimum length 6.']})

    def test_e_delete_user(self):
        with self.app() as client:
            res = client.delete('/remove/{}'.format('test1'))
            self.assertEqual(res.status_code,200)
