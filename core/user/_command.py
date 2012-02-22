from base import Database, Command
from base.Runtime import trace
import User

FAIL_REASON_USER_EXIST = "user exist"

def public_guest_create_user_account(user_id, password):
    session = Database.create_sqlalchemy_session()
    if(User.check_user_account_exist(session, user_id)):
        session.close()
        return Command.fail(reason=FAIL_REASON_USER_EXIST)
    session.close()
    pass

def public_admin_create_user_account(admin_token, user_id, password):
    pass

def public_user_remove_self_account(user_id, password):
    pass

def public_admin_remove_user_account(admin_token, user_id):
    pass

def public_user_change_self_account_password(user_id, old_password, new_password):
    pass

def public_admin_change_user_account_password(admin_token, user_id, new_password):
    pass
