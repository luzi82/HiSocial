from admin import reset
from base.Cleanup import Cleanup
from base import Database, Runtime
import HiFile._database
import pprint
import unittest
import user.User

class TestHiFile(unittest.TestCase):
    
    pp = pprint.PrettyPrinter()
    
    def setUp(self):
        reset.reset()
        Runtime.enable_trace = True

    def test_add_torrent(self):
        cleanup = Cleanup()
        session = Database.create_sqlalchemy_session_push(cleanup)
        
        user.User.add_user_account(session=session, user_id="uuuu0", password="pppp0")
        self.assertEqual(1,HiFile._database.add_torrent(session,"uuuu0"))
        self.assertEqual(2,HiFile._database.add_torrent(session,"uuuu0"))
        self.assertEqual(3,HiFile._database.add_torrent(session,"uuuu0"))
        
        self.assertEqual(HiFile._database.list_user_torrent(session,"uuuu0"),[1,2,3])
        
        self.assertEqual(HiFile._database.list_user_torrent(session,"uuuu1"),[])
