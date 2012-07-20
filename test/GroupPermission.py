from admin import reset
from base import Database, Runtime
from hs_common.hs_cleanup import Cleanup
from user import Group
import unittest
from user import GroupPermission

class GroupPermissionTest(unittest.TestCase):
    
    def setUp(self):
        Runtime.enable_trace = False
        reset.reset()
        Runtime.enable_trace = True

    def test_set(self):
        cleanup = Cleanup()
        session = Database.create_sqlalchemy_session()
        cleanup.push(session.close)

        self.assertEqual(GroupPermission.get(session,"g0","p0"),None)
        Group.add(session,"g0","G-0")
        session.flush()
        self.assertEqual("G-0", Group.get_name(session,"g0"))
        self.assertEqual(GroupPermission.get(session,"g0","p0"),None)
        GroupPermission.set(session,"g0","p0",10,True)
        session.flush()
        self.assertEqual(GroupPermission.get(session,"g0","p0"),{GroupPermission.KEY_ORDER:10,GroupPermission.KEY_ENABLE:True})
        GroupPermission.set(session,"g0","p0",5,False)
        session.flush()
        self.assertEqual(GroupPermission.get(session,"g0","p0"),{GroupPermission.KEY_ORDER:5,GroupPermission.KEY_ENABLE:False})

        pass

    def test_unset(self):
        cleanup = Cleanup()
        session = Database.create_sqlalchemy_session()
        cleanup.push(session.close)

        self.assertEqual(GroupPermission.get(session,"g0","p0"),None)
        Group.add(session,"g0","G-0")
        session.flush()
        self.assertEqual("G-0", Group.get_name(session,"g0"))
        self.assertEqual(GroupPermission.get(session,"g0","p0"),None)
        GroupPermission.set(session,"g0","p0",10,True)
        session.flush()
        self.assertEqual(GroupPermission.get(session,"g0","p0"),{GroupPermission.KEY_ORDER:10,GroupPermission.KEY_ENABLE:True})
        GroupPermission.unset(session,"g0","p0")
        session.flush()
        self.assertEqual(GroupPermission.get(session,"g0","p0"),None)

        pass
    
    def test_get(self):
        cleanup = Cleanup()
        session = Database.create_sqlalchemy_session()
        cleanup.push(session.close)

        self.assertEqual(GroupPermission.get(session,"g0","p0"),None)
        Group.add(session,"g0","G-0")
        session.flush()
        self.assertEqual("G-0", Group.get_name(session,"g0"))
        self.assertEqual(GroupPermission.get(session,"g0","p0"),None)
        GroupPermission.set(session,"g0","p0",10,True)
        session.flush()
        self.assertEqual(GroupPermission.get(session,"g0","p0"),{GroupPermission.KEY_ORDER:10,GroupPermission.KEY_ENABLE:True})
        GroupPermission.set(session,"g0","p0",5,False)
        session.flush()
        self.assertEqual(GroupPermission.get(session,"g0","p0"),{GroupPermission.KEY_ORDER:5,GroupPermission.KEY_ENABLE:False})
        GroupPermission.unset(session,"g0","p0")
        session.flush()
        self.assertEqual(GroupPermission.get(session,"g0","p0"),None)

        pass
    