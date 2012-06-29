from user import _command
from base import Runtime
from admin import reset
from user import UserLoginToken
import _testcommon
from base import hs_command

class Test_user_command(_testcommon.HsTest):

    def setUp(self):
        Runtime.enable_trace = False
        reset.reset(_testcommon)
        Runtime.enable_trace = True
        
    def test_user_create_login(self):
        ret=_command.command_guest_generate_user_login_token(_testcommon.OWNER_USERNAME,_testcommon.OWNER_PASSWORD)
        self.check_ok(ret)
        tokenA=ret[hs_command.VALUE_KEY]
        self.assertTrue(isinstance(tokenA,str))
        self.assertEqual(_testcommon.OWNER_USERNAME,UserLoginToken.check_user_login_token(tokenA))
        
        ret=_command.command_user_create_user_account(_testcommon.OWNER_USERNAME,"user0","password0")
        self.check_ok(ret)

        ret=_command.command_guest_generate_user_login_token("user0","password0")
        self.check_ok(ret)
        tokenU=ret[hs_command.VALUE_KEY]
        self.assertTrue(isinstance(tokenU,str))
        self.assertEqual("user0",UserLoginToken.check_user_login_token(tokenU))
    
    def test_guest_create_login(self):
        ret=_command.command_human_create_user_account("","","user0","password0")
        self.check_ok(ret)
        
        ret=_command.command_guest_generate_user_login_token("user0","password0")
        self.check_ok(ret)
        tokenU=ret[hs_command.VALUE_KEY]
        self.assertTrue(isinstance(tokenU,str))
        self.assertEqual("user0",UserLoginToken.check_user_login_token(tokenU))
                                  
    def test_guest_remove_user(self):
        ret=_command.command_human_create_user_account("","","user0","password0")
        self.check_ok(ret)
        
        ret=_command.command_guest_remove_user_account("user0","password0")
        self.check_ok(ret)

        ret=_command.command_guest_generate_user_login_token("user0","password0")
        self.check_fail(ret)
                                  
    def test_user_remove_user(self):
        ret=_command.command_human_create_user_account("","","user0","password0")
        self.check_ok(ret)
        
        ret=_command.command_user_remove_user_account(_testcommon.OWNER_USERNAME,"user0")
        self.check_ok(ret)

        ret=_command.command_guest_generate_user_login_token("user0","password0")
        self.check_fail(ret)
    
    def test_guest_change_user_password(self):
        ret=_command.command_human_create_user_account("","","user0","password0")
        self.check_ok(ret)
        
        ret=_command.command_guest_change_user_account_password("user0","password0","password1")
        self.check_ok(ret)

        ret=_command.command_guest_generate_user_login_token("user0","password0")
        self.check_fail(ret)
        ret=_command.command_guest_generate_user_login_token("user0","password1")
        self.check_ok(ret)

    def test_user_change_user_password(self):
        ret=_command.command_human_create_user_account("","","user0","password0")
        self.check_ok(ret)
        
        ret=_command.command_user_change_user_account_password(_testcommon.OWNER_USERNAME,"user0","password1")
        self.check_ok(ret)

        ret=_command.command_guest_generate_user_login_token("user0","password0")
        self.check_fail(ret)
        ret=_command.command_guest_generate_user_login_token("user0","password1")
        self.check_ok(ret)
    
    def test_login_user_not_exist(self):
        ret=_command.command_guest_generate_user_login_token("user1","password0")
        self.check_fail(ret)
    
    def test_login_bad_password(self):
        ret=_command.command_human_create_user_account("","","user0","password0")
        self.check_ok(ret)

        ret=_command.command_guest_generate_user_login_token("user0","password1")
        self.check_fail(ret)
        
    def test_user_no_permission(self):
        ret=_command.command_human_create_user_account("","","user0","password0")
        self.check_ok(ret)

        ret=_command.command_human_create_user_account("","","user1","password1")
        self.check_ok(ret)

        ret=_command.command_user_remove_user_account("user0","user1")
        self.check_fail(ret)

        ret=_command.command_user_change_user_account_password("user0","user1","password2")
        self.check_fail(ret)
        
    def test_create_user_already_exist(self):
        ret=_command.command_human_create_user_account("","","user0","password0")
        self.check_ok(ret)

        ret=_command.command_human_create_user_account("","","user0","password0")
        self.check_fail(ret)

        ret=_command.command_user_create_user_account(_testcommon.OWNER_USERNAME,"user0","password0")
        self.check_fail(ret)
        
    def test_remove_not_exist(self):
        ret=_command.command_guest_remove_user_account("user0","password0")
        self.check_fail(ret)

        ret=_command.command_user_remove_user_account(_testcommon.OWNER_USERNAME,"user0")
        self.check_fail(ret)

    def test_login_command(self):
#        cleanup = Cleanup()
        
        # TODO: Should put this command back to Command layer, enable backdoor for human test skip
        _command.command_human_create_user_account("", "", "uuuu0", "pppp0")

        ret=hs_command.call(
            "user","guest_generate_user_login_token",
            {
                'txt_user_id': "uuuu0",
                "txt_password": "pppp0"
            }
        )
        self.assertEqual(
            ret[hs_command.RESULT_KEY],
            hs_command.RESULT_VALUE_OK_TXT
        )
    