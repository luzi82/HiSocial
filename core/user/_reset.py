from base import Database
from base.Cleanup import Cleanup
import Group
import GroupPermission
import User
import UserGroup

def build_order():
    return 10

def build(install_config):
    if install_config != None:
        cleanup = Cleanup()
        session = Database.create_sqlalchemy_session_push(cleanup)
        
        Group.add(session, "owner", "Owner")
        GroupPermission.set(session, "owner", "admin", 99999999, True)

        User.add_user_account(session, install_config.OWNER_USERNAME, install_config.OWNER_PASSWORD)
        UserGroup.join(session, install_config.OWNER_USERNAME, "owner")
        session.commit()
