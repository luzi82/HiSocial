from admin import reset
from base import Database, Runtime
from hisocial.common.hs_cleanup import Cleanup
from base.Runtime import trace
from sqlalchemy.orm.session import sessionmaker
import unittest
from user import Group,UserGroup,User

class TestUserGroup(unittest.TestCase):

    def setUp(self):
        Runtime.enable_trace = False
        reset.reset()
        Runtime.enable_trace = True

    def test_join(self):
        cleanup = Cleanup()
        session = Database.create_sqlalchemy_session()
        cleanup.push(session.close)
        
        self.assertEqual([],UserGroup.get_group(session, "asdf"))
        User.add_user_account(session,"asdf","qwer")
        self.assertEqual([],UserGroup.get_group(session, "asdf"))
        Group.add(session, "ggg", "ddd")
        self.assertEqual([],UserGroup.get_group(session, "asdf"))
        UserGroup.join(session, "asdf", "ggg")
        self.assertEqual(["ggg"],UserGroup.get_group(session, "asdf"))

    def test_unjoin(self):
        cleanup = Cleanup()
        session = Database.create_sqlalchemy_session()
        cleanup.push(session.close)

        User.add_user_account(session,"asdf","qwer")
        Group.add(session, "ggg", "ddd")
        session.commit()
        UserGroup.join(session, "asdf", "ggg")
        self.assertEqual(["ggg"],UserGroup.get_group(session, "asdf"))
        self.assertTrue(UserGroup.unjoin(session, "asdf", "ggg"))
        self.assertEqual([],UserGroup.get_group(session, "asdf"))

    def test_get_group(self):

        cleanup = Cleanup()
        session = Database.create_sqlalchemy_session()
        cleanup.push(session.close)
        
        self.assertEqual([],UserGroup.get_group(session, "asdf"))
        User.add_user_account(session,"asdf","qwer")
        self.assertEqual([],UserGroup.get_group(session, "asdf"))
        Group.add(session, "ggg", "ddd")
        self.assertEqual([],UserGroup.get_group(session, "asdf"))
        UserGroup.join(session, "asdf", "ggg")
        self.assertEqual(["ggg"],UserGroup.get_group(session, "asdf"))
        UserGroup.unjoin(session, "asdf", "ggg")
        self.assertEqual([],UserGroup.get_group(session, "asdf"))

    def test_case0(self):
        cleanup = Cleanup()
        session = Database.create_sqlalchemy_session_push(cleanup)

        User.add_user_account(session,"uuuu0","pppp0")
        User.add_user_account(session,"uuuu1","pppp1")
        Group.add(session, "gggg0", "gggg0")
        Group.add(session, "gggg1", "gggg1")
        UserGroup.join(session, "uuuu0", "gggg0")
        UserGroup.join(session, "uuuu0", "gggg1")
        UserGroup.join(session, "uuuu1", "gggg0")
        UserGroup.join(session, "uuuu1", "gggg1")
        
        self.assertEqual(["gggg0","gggg1"],UserGroup.get_group(session, "uuuu0"))
        self.assertEqual(["gggg0","gggg1"],UserGroup.get_group(session, "uuuu1"))
