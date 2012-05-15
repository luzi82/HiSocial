from admin import reset
from base import Database, Runtime
from hisocial.common.hs_cleanup import Cleanup
from base.Runtime import trace
from sqlalchemy.orm.session import sessionmaker
import unittest
from user import Group

class TestGroup(unittest.TestCase):

    def setUp(self):
        reset.reset()
        Runtime.enable_trace = True

    def test_add(self):
        cleanup = Cleanup()
        session = Database.create_sqlalchemy_session()
        cleanup.push(session.close)
        
        self.assertEqual(None, Group.get_name(session,"asdf"))
        Group.add(session,"asdf","qwer")
        self.assertEqual("qwer", Group.get_name(session,"asdf"))

    def test_delete(self):
        cleanup = Cleanup()
        session = Database.create_sqlalchemy_session()
        cleanup.push(session.close)
        
        self.assertEqual(None, Group.get_name(session,"asdf"))
        Group.add(session,"asdf","qwer")
        self.assertEqual("qwer", Group.get_name(session,"asdf"))
        self.assertTrue(Group.delete(session,"asdf"))
        self.assertEqual(None, Group.get_name(session,"asdf"))
        self.assertFalse(Group.delete(session,"asdf"))

        self.assertFalse(Group.delete(session,"xxx"))

    def test_rename(self):
        cleanup = Cleanup()
        session = Database.create_sqlalchemy_session()
        cleanup.push(session.close)
        
        Group.add(session,"asdf","qwer")
        self.assertEqual("qwer", Group.get_name(session,"asdf"))
        self.assertNotEqual("zxcv", Group.get_name(session,"asdf"))
        self.assertTrue(Group.rename(session,"asdf","zxcv"))
        self.assertEqual("zxcv", Group.get_name(session,"asdf"))
        self.assertNotEqual("qwer", Group.get_name(session,"asdf"))

        self.assertFalse(Group.rename(session,"xxx","xxx"))

    def test_get_name(self):
        cleanup = Cleanup()
        session = Database.create_sqlalchemy_session()
        cleanup.push(session.close)
        
        self.assertEqual(None, Group.get_name(session,"asdf"))
        Group.add(session,"asdf","qwer")
        self.assertEqual("qwer", Group.get_name(session,"asdf"))
