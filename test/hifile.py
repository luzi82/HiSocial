from admin import reset
from base import Database, Runtime
from base.Cleanup import Cleanup
import HiFile.TorrentStorage
import HiFile._command
import HiFile._database
import binascii
import filecmp
import pprint
import unittest
import user.User
import user.UserLoginToken

class TestHiFile(unittest.TestCase):
    
    pp = pprint.PrettyPrinter()
    
    def setUp(self):
        Runtime.enable_trace = False
        reset.reset()
        Runtime.enable_trace = True

    def test_add_torrent(self):
        cleanup = Cleanup()
        session = Database.create_sqlalchemy_session_push(cleanup)
        
        user.User.add_user_account(session=session, user_id="uuuu0", password="pppp0")
        self.assertEqual(1,HiFile._database.add_torrent(session,"uuuu0","0123456789012345678901234567890123456789"))
        self.assertEqual(2,HiFile._database.add_torrent(session,"uuuu0","0123456789012345678901234567890123456789"))
        self.assertEqual(3,HiFile._database.add_torrent(session,"uuuu0","0123456789012345678901234567890123456789"))
        
        self.assertEqual(HiFile._database.list_user_torrent(session,"uuuu0"),[1,2,3])
        
        self.assertEqual(HiFile._database.list_user_torrent(session,"uuuu1"),[])

    def test_torrentid_to_path(self):
        self.assertEqual(HiFile.TorrentStorage._torrentid_to_path(0x1),HiFile.TorrentStorage.STORAGE_PATH+"/00000001")
        self.assertEqual(HiFile.TorrentStorage._torrentid_to_path(0xa),HiFile.TorrentStorage.STORAGE_PATH+"/0000000a")
        self.assertEqual(HiFile.TorrentStorage._torrentid_to_path(0xabc123),HiFile.TorrentStorage.STORAGE_PATH+"/00abc123")

    def test_command_user_upload_torrent(self):
        cleanup = Cleanup()

        session = Database.create_sqlalchemy_session_push(cleanup)
        user.User.add_user_account(session=session, user_id="uuuu0", password="pppp0")
        cleanup.clean_all()

        user_login_token=user.UserLoginToken.generate_user_login_token("uuuu0")

        torrent_file=open("res/test0.torrent","rb")
        ret=HiFile._command.public_user_upload_torrent(user_login_token, torrent_file)
        self.assertEqual(ret,{"result":"ok","torrent_id":1})
        torrent_file.close()
        
        session = Database.create_sqlalchemy_session_push(cleanup)
        self.assertTrue(filecmp.cmp("res/test0.torrent",HiFile.TorrentStorage._torrentid_to_path(0x1)))
        self.assertEqual(HiFile._database.list_user_torrent(session,"uuuu0"),[1])
        
        r=session.query(HiFile.TrackerManager.XBT_FILES).all()
        self.assertEqual(len(r),1)
        self.assertEqual(binascii.b2a_hex(r[0].info_hash),"2034385a2621c53a490f34c5893a860664741da4")
        
        r=session.query(HiFile._database.Torrent).all()
        self.assertEqual(len(r),1)
        self.assertEqual(r[0].torrent_id,1)
        self.assertEqual(r[0].user_id,"uuuu0")
        self.assertEqual(binascii.b2a_hex(r[0].info_hash_bin),"2034385a2621c53a490f34c5893a860664741da4")
