from basetest import BaseTest
from services.models.UserModel import UserModel
from services.serve import bcrypt

class UserTest(BaseTest):
    def test_create_user(self):
        user = UserModel('oman','asdasd')
        self.assertEqual(user.username,'oman')
        self.assertTrue(bcrypt.check_password_hash(user.password,'asdasd'))
