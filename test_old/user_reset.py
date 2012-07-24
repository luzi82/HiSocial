import unittest
from user import User,UserGroup,Permission
from hs_common.hs_cleanup import Cleanup
from base import Database, Runtime
from admin import reset
import _testcommon

class TestUserPackage(unittest.TestCase):
    
    def setUp(self):
        Runtime.enable_trace = False
        reset.reset(_testcommon)
        Runtime.enable_trace = True
    
    def test_owner(self):
        cleanup = Cleanup()
        session = Database.create_sqlalchemy_session_push(cleanup)
        
        self.assertTrue(User.check_user_account_exist(session,_testcommon.OWNER_USERNAME))
        self.assertTrue(User.check_user_account_password(session,_testcommon.OWNER_USERNAME,_testcommon.OWNER_PASSWORD))
        self.assertTrue(UserGroup.get_group(session,_testcommon.OWNER_USERNAME),["owner"])
        self.assertTrue(Permission.get_user_permission(session, _testcommon.OWNER_USERNAME, "admin"))
