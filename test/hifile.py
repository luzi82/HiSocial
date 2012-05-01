# -*- coding: utf-8 -*-

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
import time

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
        self.assertEqual(1,HiFile._database.add_torrent(session,"uuuu0","0123456789012345678901234567890123456789","name",123))
        self.assertEqual(2,HiFile._database.add_torrent(session,"uuuu0","0123456789012345678901234567890123456789","name",123))
        self.assertEqual(3,HiFile._database.add_torrent(session,"uuuu0","0123456789012345678901234567890123456789","name",123))
        
        self.assertEqual(HiFile._database.list_user_torrent(session,"uuuu0"),[ \
            { \
                "torrent_id":3, \
                "user_id":"uuuu0", \
                "info_hash_bin":"0123456789012345678901234567890123456789", \
                "name":"name", \
                "size":123, \
            }, \
            { \
                "torrent_id":2, \
                "user_id":"uuuu0", \
                "info_hash_bin":"0123456789012345678901234567890123456789", \
                "name":"name", \
                "size":123, \
            }, \
            { \
                "torrent_id":1, \
                "user_id":"uuuu0", \
                "info_hash_bin":"0123456789012345678901234567890123456789", \
                "name":"name", \
                "size":123, \
            }, \
        ])
        
        self.assertEqual(HiFile._database.list_user_torrent(session,"uuuu1"),[])

    def test_torrentid_to_path(self):
        self.assertEqual(HiFile.TorrentStorage._torrentid_to_path(0x1),HiFile.TorrentStorage.STORAGE_PATH+"/00000001")
        self.assertEqual(HiFile.TorrentStorage._torrentid_to_path(0xa),HiFile.TorrentStorage.STORAGE_PATH+"/0000000a")
        self.assertEqual(HiFile.TorrentStorage._torrentid_to_path(0xabc123),HiFile.TorrentStorage.STORAGE_PATH+"/00abc123")

    def test_command_user_upload_torrent(self):
        cleanup = Cleanup()

        session = Database.create_sqlalchemy_session_push(cleanup)
        user.User.add_user_account(session=session, user_id="uuuu0", password="pppp0")
        session.flush()
        session.commit()
        cleanup.clean_all()

        user_login_token=user.UserLoginToken.generate_user_login_token("uuuu0")

        torrent_file=open("res/test0.torrent","rb")
        ret=HiFile._command.command_user_upload_torrent(user_login_token, torrent_file)
        self.assertEqual(ret,{"result":"ok","torrent_id":1})
        torrent_file.close()
        
        session = Database.create_sqlalchemy_session_push(cleanup)
        
        self.assertTrue(filecmp.cmp("res/test0.torrent",HiFile.TorrentStorage._torrentid_to_path(0x1)))
        self.assertEqual(HiFile._database.list_user_torrent(session,"uuuu0"), [ \
            { \
                "torrent_id":1, \
                "user_id":"uuuu0", \
                "info_hash_bin":"2034385a2621c53a490f34c5893a860664741da4", \
                "name":"Super Eurobeat Vol. 220 - Anniversary Hits",\
                "size":365751495 \
            } \
        ])
        
        r=session.query(HiFile.TrackerManager.XBT_FILES).all()
        self.assertEqual(len(r),1)
        self.assertEqual(binascii.b2a_hex(r[0].info_hash),"2034385a2621c53a490f34c5893a860664741da4")
        
        r=session.query(HiFile._database.Torrent).all()
        self.assertEqual(len(r),1)
        self.assertEqual(r[0].torrent_id,1)
        self.assertEqual(r[0].user_id,"uuuu0")
        self.assertEqual(r[0].name,"Super Eurobeat Vol. 220 - Anniversary Hits")
        self.assertEqual(r[0].size,365751495)
        self.assertEqual(binascii.b2a_hex(r[0].info_hash_bin),"2034385a2621c53a490f34c5893a860664741da4")

        cleanup.clean_all()
        
        ret=HiFile._command.command_user_list_user_torrent(user_login_token, "uuuu0")
        self.assertEqual(len(ret),2)
        self.assertEqual(ret["result"],"ok")
        ret_torrent_list=ret["torrent_list"]
        self.assertEqual(len(ret_torrent_list),1)
        self.assertEqual(len(ret_torrent_list[0]),4)
        self.assertEqual(ret_torrent_list[0]["torrent_id"],1)
        self.assertEqual(ret_torrent_list[0]["name"],"Super Eurobeat Vol. 220 - Anniversary Hits")
        self.assertEqual(ret_torrent_list[0]["size"],365751495)
        self.assertNotEquals(ret_torrent_list[0]["torrent_token"],None)

        torrent_file=open("res/test2.torrent","rb")
        ret=HiFile._command.command_user_upload_torrent(user_login_token, torrent_file)
        self.assertEqual(ret,{"result":"ok","torrent_id":2})
        torrent_file.close()

        session = Database.create_sqlalchemy_session_push(cleanup)
        
        self.assertTrue(filecmp.cmp("res/test2.torrent",HiFile.TorrentStorage._torrentid_to_path(0x2)))
        self.assertEqual(HiFile._database.list_user_torrent(session,"uuuu0"),[ \
            { \
                "torrent_id":2, \
                "user_id":"uuuu0", \
                "info_hash_bin":"39eaf2230aa0bcf9148f84f6efe0c64cc1ab80c1", \
                "name":"魔法少女小圓",\
                "size":616839726 \
            }, \
            { \
                "torrent_id":1, \
                "user_id":"uuuu0", \
                "info_hash_bin":"2034385a2621c53a490f34c5893a860664741da4", \
                "name":"Super Eurobeat Vol. 220 - Anniversary Hits",\
                "size":365751495 \
            }, \
        ])

        r=session.query(HiFile.TrackerManager.XBT_FILES).count()
        self.assertEqual(r,2)

        r=session.query(HiFile._database.Torrent).count()
        self.assertEqual(r,2)
        
        r=session.query(HiFile._database.Torrent).filter(HiFile._database.Torrent.info_hash_bin==binascii.a2b_hex("39eaf2230aa0bcf9148f84f6efe0c64cc1ab80c1")).all()
        self.assertEqual(len(r),1)
        self.assertEqual(r[0].torrent_id,2)
        self.assertEqual(r[0].user_id,"uuuu0")
        self.assertEqual(r[0].name,"魔法少女小圓")
        self.assertEqual(r[0].size,616839726)
        self.assertEqual(binascii.b2a_hex(r[0].info_hash_bin),"39eaf2230aa0bcf9148f84f6efe0c64cc1ab80c1")

        cleanup.clean_all()

        torrent_file=open("res/test3.torrent","rb")
        ret=HiFile._command.command_user_upload_torrent(user_login_token, torrent_file)
        self.assertEqual(ret,{"result":"ok","torrent_id":3})
        torrent_file.close()

        session = Database.create_sqlalchemy_session_push(cleanup)

        r=session.query(HiFile._database.Torrent).filter(HiFile._database.Torrent.info_hash_bin==binascii.a2b_hex("da5142099da45138ebbab05a40664c98ac2c0496")).all()
        self.assertEqual(len(r),1)
        self.assertEqual(r[0].torrent_id,3)
        self.assertEqual(r[0].user_id,"uuuu0")
        self.assertEqual(r[0].name,"[CASO&SumiSora][Puella_Magi_Madoka_Magica][BDRIP][GB_BIG5]")
        self.assertEqual(r[0].size,20185116425)
        self.assertEqual(binascii.b2a_hex(r[0].info_hash_bin),"da5142099da45138ebbab05a40664c98ac2c0496")

        cleanup.clean_all()

    def test_torrent_token(self):
        now = int(time.time())
        
        token = HiFile.generate_torrent_token(123,now,now+1000,"uuuu0")
        self.assertEqual(123,HiFile.verify_torrent_token(token))

        token = HiFile.generate_torrent_token(123,now+1000,now+2000,"uuuu0")
        self.assertEqual(None,HiFile.verify_torrent_token(token))

        token = HiFile.generate_torrent_token(123,now-2000,now-1000,"uuuu0")
        self.assertEqual(None,HiFile.verify_torrent_token(token))

    def test_get_torrent_data(self):
        cleanup = Cleanup()

        session = Database.create_sqlalchemy_session_push(cleanup)
        user.User.add_user_account(session=session, user_id="uuuu0", password="pppp0")
        session.flush()
        session.commit()
        cleanup.clean_all()

        user_login_token=user.UserLoginToken.generate_user_login_token("uuuu0")
        
        torrent_file=open("res/test0.torrent","rb")
        ret=HiFile._command.command_user_upload_torrent(user_login_token, torrent_file)
        self.assertEqual(ret,{"result":"ok","torrent_id":1})
        torrent_file.close()

        session = Database.create_sqlalchemy_session_push(cleanup)
        ret = HiFile._database.get_torrent_data(session,1)
        self.assertEqual(ret["torrent_id"],1)
        self.assertEqual(ret["user_id"],"uuuu0")
        self.assertEqual(ret["info_hash_bin"],"2034385a2621c53a490f34c5893a860664741da4")
        self.assertEqual(ret["name"],"Super Eurobeat Vol. 220 - Anniversary Hits")
        self.assertEqual(ret["size"],365751495)

#    def test_get_torrent_file(self):
#        cleanup = Cleanup()
#
#        session = Database.create_sqlalchemy_session_push(cleanup)
#        user.User.add_user_account(session=session, user_id="uuuu0", password="pppp0")
#        self.assertEqual(1,HiFile._database.add_torrent(session,"uuuu0","0123456789012345678901234567890123456789","name",123))
#        session.flush()
#        session.commit()
#        cleanup.clean_all()
