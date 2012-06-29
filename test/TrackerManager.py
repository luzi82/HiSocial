from HiFile import TrackerManager
from base import Runtime, Database
from hs_common.hs_cleanup import Cleanup
import pprint
import unittest
from admin import reset

class TrackerManagerTest(unittest.TestCase):
    
    def setUp(self):
        reset.reset()
        Runtime.enable_trace = True
        Runtime.enable_debug = True

    def test_session(self):
        cleanup = Cleanup()
        session = Database.create_sqlalchemy_session_push(cleanup)
        
        c = session.query(TrackerManager.XBT_FILES).count();
        self.assertEqual(c, 0)
        
        session.add(TrackerManager.XBT_FILES(info_hash="01234567890123456789",mtime=0,ctime=0))
        session.flush()
        
        c = session.query(TrackerManager.XBT_FILES).count();
        self.assertEqual(c, 1)

    def test_api(self):
        cleanup = Cleanup()
        session = Database.create_sqlalchemy_session_push(cleanup)

        c = session.query(TrackerManager.XBT_FILES).count();
        self.assertEqual(c, 0)
        
        TrackerManager.add_hash(session, "01234567890123456789")
        
        c = session.query(TrackerManager.XBT_FILES).count();
        self.assertEqual(c, 1)
        