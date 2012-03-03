from base import Runtime
from base.Runtime import trace
from user import UserLoginToken
import time
import unittest

class UserLoginTokenTest(unittest.TestCase):

    def setUp(self):
        Runtime.enable_trace = True

    def test_token(self):
        token = UserLoginToken.generate_user_login_token("u0")
        trace(token)
        self.assertEqual(UserLoginToken.check_user_login_token(token),"u0")
        
        old_token = UserLoginToken.generate_user_login_token("u0",int(time.time())-10)
        trace(old_token)
        self.assertEqual(UserLoginToken.check_user_login_token(old_token),None)

if __name__ == '__main__':
    unittest.main()
