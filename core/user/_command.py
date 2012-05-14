from base import Database, Command
from base.Runtime import trace
import User,UserLoginToken
from hisocial.common.Cleanup import Cleanup
from turing import turing
from user import Permission

FAIL_REASON_USER_EXIST = "user exist"

def command_guest_generate_user_login_token(txt_user_id, txt_password):
    '''
    Generate admin token
    '''
    cleanup = Cleanup()
    session = Database.create_sqlalchemy_session_push(cleanup)

    if not User.check_user_account_password(session, txt_user_id, txt_password):
        return Command.fail(reason="auth")

    cleanup.clean_all();

    token = UserLoginToken.generate_user_login_token(txt_user_id)
    
    return Command.ok(value=token)

def command_human_create_user_account(txtf_turing_turing,env_ip,txt_user_id, txt_password):

    cleanup = Cleanup()
    session = Database.create_sqlalchemy_session_push(cleanup)

    if(User.check_user_account_exist(session, txt_user_id)):
        return Command.fail(reason=FAIL_REASON_USER_EXIST)
    
    User.add_user_account(session, txt_user_id, txt_password)
    
    session.commit()
    cleanup.clean_all();

    token = UserLoginToken.generate_user_login_token(txt_user_id)
    
    return Command.ok({"user_login_token":token})

def command_user_create_user_account(txtf_user_token,txt_user_id, txt_password):
    cleanup = Cleanup()
    session = Database.create_sqlalchemy_session_push(cleanup)
    
    if not Permission.get_user_permission(session, txtf_user_token, "admin"):
        return Command.fail(reason="permission")
    
    if User.check_user_account_exist(session, txt_user_id):
        return Command.fail(reason=FAIL_REASON_USER_EXIST)

    User.add_user_account(session, txt_user_id, txt_password)
    
    session.commit()
    cleanup.clean_all();
    
    return Command.ok()

def command_guest_remove_user_account(txt_user_id, txt_password):
    cleanup = Cleanup()
    session = Database.create_sqlalchemy_session_push(cleanup)
    
    if not User.check_user_account_password(session, txt_user_id, txt_password):
        return Command.fail(reason="auth")
    
    User.remove_user_account(session, txt_user_id)
    session.commit()
    cleanup.clean_all();

    return Command.ok()

def command_user_remove_user_account(txtf_user_token, txt_user_id):
    cleanup = Cleanup()
    session = Database.create_sqlalchemy_session_push(cleanup)
    
    if not Permission.get_user_permission(session, txtf_user_token, "admin"):
        return Command.fail(reason="permission")
    
    if not User.check_user_account_exist(session, txt_user_id):
        return Command.fail(reason="user_id")
    
    User.remove_user_account(session, txt_user_id)
    session.commit()
    cleanup.clean_all();

    return Command.ok()

def command_guest_change_user_account_password(txt_user_id, txt_old_password, txt_new_password):
    cleanup = Cleanup()
    session = Database.create_sqlalchemy_session_push(cleanup)
    
    if not User.check_user_account_password(session, txt_user_id, txt_old_password):
        return Command.fail(reason="auth")
    
    User.change_password(session, txt_user_id, txt_new_password)
    session.commit()
    cleanup.clean_all();

    return Command.ok()

def command_user_change_user_account_password(txtf_user_token, txt_user_id, txt_new_password):
    cleanup = Cleanup()
    session = Database.create_sqlalchemy_session_push(cleanup)
    
    if not Permission.get_user_permission(session, txtf_user_token, "admin"):
        return Command.fail(reason="permission")
    
    if not User.check_user_account_exist(session, txt_user_id):
        return Command.fail(reason="txt_user_id")

    User.change_password(session, txt_user_id, txt_new_password)
    session.commit()
    cleanup.clean_all();
    
    return Command.ok()

def argfilter_token(v):
    ret = UserLoginToken.check_user_login_token(v)
    if ret == None:
        return Command.fail(reason="bad user token")
    return Command.ok(value=ret)
