from admin import AdminToken
from base import Runtime
from base.Runtime import trace
import time
import unittest

class AdminTokenTest(unittest.TestCase):

    def setUp(self):
        Runtime.enable_trace = True

    def test_token(self):
        token = AdminToken.generate_admin_token()
        trace(token)
        self.assertTrue(AdminToken.check_admin_token(token))
        
        old_token = AdminToken.generate_admin_token(int(time.time())-10)
        trace(old_token)
        self.assertFalse(AdminToken.check_admin_token(old_token))

if __name__ == '__main__':
    unittest.main()
