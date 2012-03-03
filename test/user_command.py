import unittest
from user import _command
from base.Cleanup import Cleanup
from base import Database, Runtime
from admin import reset
from base.Runtime import trace
from turing import turing
from user import UserLoginToken

class Test_user_command(unittest.TestCase):

    OWNER_USERNAME="akari"
    OWNER_PASSWORD="mizunashi"
    
    def setUp(self):
        turing.force_output=None
        Runtime.enable_trace = False
        reset.reset(self)
        Runtime.enable_trace = True
        
    def test_user_create_login(self):
        ret=_command.public_guest_generate_user_login_token(self.OWNER_USERNAME,self.OWNER_PASSWORD)
        self.check_ok(ret)
        tokenA=ret["user_login_token"]
        self.assertTrue(isinstance(tokenA,str))
        self.assertEqual(self.OWNER_USERNAME,UserLoginToken.check_user_login_token(tokenA))
        
        ret=_command.public_user_create_user_account(tokenA,"user0","password0")
        self.check_ok(ret)

        ret=_command.public_guest_generate_user_login_token("user0","password0")
        self.check_ok(ret)
        tokenU=ret["user_login_token"]
        self.assertTrue(isinstance(tokenU,str))
        self.assertEqual("user0",UserLoginToken.check_user_login_token(tokenU))
    
    def test_guest_create_login(self):
        turing.force_output=True
        
        ret=_command.public_human_create_user_account("","","user0","password0")
        self.check_ok(ret)
        
        ret=_command.public_guest_generate_user_login_token("user0","password0")
        self.check_ok(ret)
        tokenU=ret["user_login_token"]
        self.assertTrue(isinstance(tokenU,str))
        self.assertEqual("user0",UserLoginToken.check_user_login_token(tokenU))
                                  
    def test_guest_remove_user(self):
        turing.force_output=True
        
        ret=_command.public_human_create_user_account("","","user0","password0")
        self.check_ok(ret)
        
        ret=_command.public_guest_remove_user_account("user0","password0")
        self.check_ok(ret)

        ret=_command.public_guest_generate_user_login_token("user0","password0")
        self.check_fail(ret)
                                  
    def test_user_remove_user(self):
        turing.force_output=True

        ret=_command.public_guest_generate_user_login_token(self.OWNER_USERNAME,self.OWNER_PASSWORD)
        self.check_ok(ret)
        token0=ret["user_login_token"]

        ret=_command.public_human_create_user_account("","","user0","password0")
        self.check_ok(ret)
        
        ret=_command.public_user_remove_user_account(token0,"user0")
        self.check_ok(ret)

        ret=_command.public_guest_generate_user_login_token("user0","password0")
        self.check_fail(ret)
    
    def test_guest_change_user_password(self):
        turing.force_output=True
        
        ret=_command.public_human_create_user_account("","","user0","password0")
        self.check_ok(ret)
        
        ret=_command.public_guest_change_user_account_password("user0","password0","password1")
        self.check_ok(ret)

        ret=_command.public_guest_generate_user_login_token("user0","password0")
        self.check_fail(ret)
        ret=_command.public_guest_generate_user_login_token("user0","password1")
        self.check_ok(ret)

    def test_user_change_user_password(self):
        turing.force_output=True

        ret=_command.public_guest_generate_user_login_token(self.OWNER_USERNAME,self.OWNER_PASSWORD)
        self.check_ok(ret)
        tokenA=ret["user_login_token"]

        ret=_command.public_human_create_user_account("","","user0","password0")
        self.check_ok(ret)
        
        ret=_command.public_user_change_user_account_password(tokenA,"user0","password1")
        self.check_ok(ret)

        ret=_command.public_guest_generate_user_login_token("user0","password0")
        self.check_fail(ret)
        ret=_command.public_guest_generate_user_login_token("user0","password1")
        self.check_ok(ret)
    
    def test_login_user_not_exist(self):
        ret=_command.public_guest_generate_user_login_token("user1","password0")
        self.check_fail(ret)
    
    def test_login_bad_password(self):
        turing.force_output=True

        ret=_command.public_guest_generate_user_login_token("user0","password1")
        self.check_fail(ret)
        
    def test_user_no_permission(self):
        turing.force_output=True
        
        ret=_command.public_human_create_user_account("","","user0","password0")
        self.check_ok(ret)

        ret=_command.public_human_create_user_account("","","user1","password1")
        self.check_ok(ret)

        ret=_command.public_guest_generate_user_login_token("user0","password0")
        self.check_ok(ret)
        tokenU=ret["user_login_token"]
        
        ret=_command.public_user_remove_user_account(tokenU,"user1")
        self.check_fail(ret)

        ret=_command.public_user_change_user_account_password(tokenU,"user1","password2")
        self.check_fail(ret)
        
    def test_create_user_already_exist(self):
        turing.force_output=True

        ret=_command.public_human_create_user_account("","","user0","password0")
        self.check_ok(ret)

        ret=_command.public_human_create_user_account("","","user0","password0")
        self.check_fail(ret)

        ret=_command.public_guest_generate_user_login_token(self.OWNER_USERNAME,self.OWNER_PASSWORD)
        self.check_ok(ret)
        tokenA=ret["user_login_token"]

        ret=_command.public_user_create_user_account(tokenA,"user0","password0")
        self.check_fail(ret)
        
    def check_ok(self,result):
        self.assertTrue(result["result"]=="ok")

    def check_fail(self,result):
        self.assertTrue(result["result"]=="fail")
    