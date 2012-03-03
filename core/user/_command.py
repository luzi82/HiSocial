from base import Database, Command
from base.Runtime import trace
import User,UserLoginToken
from base.Cleanup import Cleanup

FAIL_REASON_USER_EXIST = "user exist"

def public_guest_generate_user_login_token(user_id, password):
    '''
    Generate admin token
    '''
    cleanup = Cleanup()
    session = Database.create_sqlalchemy_session_push(cleanup)

    if not User.check_user_account_password(session, user_id, password):
        return Command.fail(reason="auth err")

    token = UserLoginToken.generate_user_login_token(user_id)
    return Command.ok({"user_login_token":token})

def public_guest_create_user_account(user_id, password):
    cleanup = Cleanup()
    session = Database.create_sqlalchemy_session_push(cleanup)

    if(User.check_user_account_exist(session, user_id)):
        return Command.fail(reason=FAIL_REASON_USER_EXIST)
    return Command.ok()

def public_user_remove_self_account(user_id, password):
    pass

def public_admin_remove_user_account(admin_token, user_id):
    pass

def public_user_change_self_account_password(user_id, old_password, new_password):
    pass

def public_admin_change_user_account_password(admin_token, user_id, new_password):
    pass
