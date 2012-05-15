from Crypto.Cipher import AES
from base import Runtime
from base.Runtime import trace
from hisocial.common import hs_random
from user import UserLoginToken
import base64
import time
import unittest

class UserLoginTokenTest(unittest.TestCase):

    def setUp(self):
        Runtime.enable_trace = True
        Runtime.enable_debug = True

    def test_token(self):
        token = UserLoginToken.generate_user_login_token("u0")
#        trace(token)
        self.assertEqual(UserLoginToken.check_user_login_token(token),"u0")
        
        old_token = UserLoginToken.generate_user_login_token("u0",int(time.time())-10)
#        trace(old_token)
        self.assertEqual(UserLoginToken.check_user_login_token(old_token),None)

    def test_crazy(self):
        self.assertEqual(UserLoginToken.check_user_login_token(""),None)
        self.assertEqual(UserLoginToken.check_user_login_token("asdf"),None)
        self.assertEqual(UserLoginToken.check_user_login_token("@%!%$!@#$!%"),None)
        for i in xrange(100):
            x = hs_random.random_byte(AES.block_size*i)
            x = base64.b64encode(x)
            self.assertEqual(UserLoginToken.check_user_login_token(x),None)

if __name__ == '__main__':
    unittest.main()
