from base import Database, Command
from base.Runtime import trace
import User,UserLoginToken
from base.Cleanup import Cleanup
from turing import turing
from user import Permission

FAIL_REASON_USER_EXIST = "user exist"

def public_guest_generate_user_login_token(user_id, password):
    '''
    Generate admin token
    '''
    cleanup = Cleanup()
    session = Database.create_sqlalchemy_session_push(cleanup)

    if not User.check_user_account_password(session, user_id, password):
        return Command.fail(reason="auth")

    token = UserLoginToken.generate_user_login_token(user_id)
    
    return Command.ok({"user_login_token":token})

def public_human_create_user_account(turing_value,_ip,user_id, password):
    if not turing.check_recaptcha(turing_value, _ip):
        return Command.fail(reason="turing")
    
    cleanup = Cleanup()
    session = Database.create_sqlalchemy_session_push(cleanup)

    if(User.check_user_account_exist(session, user_id)):
        return Command.fail(reason=FAIL_REASON_USER_EXIST)
    
    User.add_user_account(session, user_id, password)
    
    session.commit()
    
    return Command.ok()

def public_user_create_user_account(user_login_token,user_id, password):
    actor_id = UserLoginToken.check_user_login_token(user_login_token)
    if actor_id == None:
        return Command.fail(reason="user_login_token")
    
    cleanup = Cleanup()
    session = Database.create_sqlalchemy_session_push(cleanup)
    
    if not Permission.get_user_permission(session, actor_id, "admin"):
        return Command.fail(reason="permission")
    
    if User.check_user_account_exist(session, user_id):
        return Command.fail(reason=FAIL_REASON_USER_EXIST)

    User.add_user_account(session, user_id, password)
    
    session.commit()
    
    return Command.ok()

def public_guest_remove_user_account(user_id, password):
    cleanup = Cleanup()
    session = Database.create_sqlalchemy_session_push(cleanup)
    
    if not User.check_user_account_password(session, user_id, password):
        return Command.fail(reason="auth")
    
    User.remove_user_account(session, user_id)
    session.commit()

    return Command.ok()

def public_user_remove_user_account(user_login_token, user_id):
    actor_id = UserLoginToken.check_user_login_token(user_login_token)
    
    if actor_id == None:
        return Command.fail(reason="user_login_token")

    cleanup = Cleanup()
    session = Database.create_sqlalchemy_session_push(cleanup)
    
    if not Permission.get_user_permission(session, actor_id, "admin"):
        return Command.fail(reason="permission")
    
    if not User.check_user_account_exist(session, user_id):
        return Command.fail(reason="user_id")
    
    User.remove_user_account(session, user_id)
    session.commit()

    return Command.ok()

def public_guest_change_user_account_password(user_id, old_password, new_password):
    cleanup = Cleanup()
    session = Database.create_sqlalchemy_session_push(cleanup)
    
    if not User.check_user_account_password(session, user_id, old_password):
        return Command.fail(reason="auth")
    
    User.change_password(session, user_id, new_password)
    session.commit()
    
    return Command.ok()

def public_user_change_user_account_password(user_login_token, user_id, new_password):
    actor_id = UserLoginToken.check_user_login_token(user_login_token)
    
    if actor_id == None:
        return Command.fail(reason="user_login_token")

    cleanup = Cleanup()
    session = Database.create_sqlalchemy_session_push(cleanup)
    
    if not Permission.get_user_permission(session, actor_id, "admin"):
        return Command.fail(reason="permission")
    
    if not User.check_user_account_exist(session, user_id):
        return Command.fail(reason="user_id")

    User.change_password(session, user_id, new_password)
    session.commit()
    
    return Command.ok()
