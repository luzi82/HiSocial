import unittest
from user import User,UserGroup,Permission
from base.Cleanup import Cleanup
from base import Database, Runtime
from admin import reset
from base.Runtime import trace

class TestUserPackage(unittest.TestCase):
    
    OWNER_USERNAME="akari"
    OWNER_PASSWORD="mizunashi"

    def setUp(self):
        Runtime.enable_trace = False
        reset.reset(self)
        Runtime.enable_trace = True
    
    def test_owner(self):
        cleanup = Cleanup()
        session = Database.create_sqlalchemy_session_push(cleanup)
        
        self.assertTrue(User.check_user_account_exist(session,self.OWNER_USERNAME))
        self.assertTrue(User.check_user_account_password(session,self.OWNER_USERNAME,self.OWNER_PASSWORD))
        self.assertTrue(UserGroup.get_group(session,self.OWNER_USERNAME),["owner"])
        self.assertTrue(Permission.get_user_permission(session, self.OWNER_USERNAME, "admin"))