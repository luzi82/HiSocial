import unittest
import install_config
from user import User,UserGroup,Permission
from base.Cleanup import Cleanup
from base import Database, Runtime
from admin import reset
from base.Runtime import trace

class TestUserPackage(unittest.TestCase):
    
    def setUp(self):
        Runtime.enable_trace = True
        reset.reset(install_config)
        Runtime.enable_trace = True
    
    def test_owner(self):
        cleanup = Cleanup()
        session = Database.create_sqlalchemy_session_push(cleanup)
        
        self.assertTrue(User.check_user_account_exist(session,install_config.OWNER_USERNAME))
        self.assertTrue(User.check_user_account_password(session,install_config.OWNER_USERNAME,install_config.OWNER_PASSWORD))
        self.assertTrue(UserGroup.get_group(session,install_config.OWNER_USERNAME),["owner"])
        self.assertTrue(Permission.get_user_permission(session, install_config.OWNER_USERNAME, "admin"))
