from admin import reset
from base import Database, Runtime
from hs_common.hs_cleanup import Cleanup
from user import User,UserGroup,Group,GroupPermission,Permission
import unittest

class PermissionTest(unittest.TestCase):

    def setUp(self):
        Runtime.enable_trace = False
        reset.reset()
        Runtime.enable_trace = True

    def test_get_user_permission(self):
        cleanup = Cleanup()
        session = Database.create_sqlalchemy_session()
        cleanup.push(session.close)
        
        User.add_user_account(session, "u0", "up0")
        Group.add(session, "g0", "g0")
        UserGroup.join(session, "u0", "g0")
        self.assertEqual(Permission.get_user_permission(session, "u0", "p0"), False)
        GroupPermission.set(session, "g0", "p0", 10, True)
        self.assertEqual(Permission.get_user_permission(session, "u0", "p0"), True)
        GroupPermission.set(session, "g0", "p0", 20, False)
        self.assertEqual(Permission.get_user_permission(session, "u0", "p0"), False)
        Group.add(session, "g1", "g1")
        UserGroup.join(session, "u0", "g1")
        GroupPermission.set(session, "g1", "p0", 30, True)
        self.assertEqual(Permission.get_user_permission(session, "u0", "p0"), True)

        self.assertEqual(Permission.get_user_permission(session, "u1", "p0"), False)
        self.assertEqual(Permission.get_user_permission(session, "u0", "p1"), False)
