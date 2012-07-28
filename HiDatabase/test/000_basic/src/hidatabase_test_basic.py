import unittest
import hiframe
import os
import shutil
from hs_common.hs_cleanup import Cleanup
from hidatabase_test_basic_plugin._hiframe import TestTable
import hashlib
import hidatabase

MY_ABSOLUTE_PATH = os.path.abspath(__file__)
TEST_SRC_PATH = os.path.dirname(MY_ABSOLUTE_PATH)
TEST_PATH = os.path.dirname(TEST_SRC_PATH)
PLUGIN_PATH = os.path.dirname(os.path.dirname(TEST_PATH))
PLUGIN_SRC_PATH = PLUGIN_PATH+"/src"

DATA_PATH = TEST_PATH+"/tmp"
DB_FILE = DATA_PATH+"/HiDatabase/tmp.sqlite3"
CONF_FILE = TEST_PATH+"/res/setting.conf"

class HidatabaseTestBasic(unittest.TestCase):

    def setUp(self):
        os.chdir(TEST_PATH)
        if os.path.exists(DATA_PATH):
            shutil.rmtree(DATA_PATH)

    def tearDown(self):
        if os.path.exists(DATA_PATH):
            shutil.rmtree(DATA_PATH)

    def test_basic(self):
        hf = hiframe.HiFrame(plugin_path_list=[TEST_SRC_PATH,PLUGIN_SRC_PATH],conf_file=CONF_FILE)

        hf.build()
        self.assertTrue(os.path.exists(DB_FILE))
        md5_0 = hashlib.md5(file(DB_FILE,"r").read())

        hf.start()

        session = hidatabase.create_sqlalchemy_session()
        new_row = TestTable(rid=0,data="zero")
        session.add(new_row)
        session.flush()
        session.close()

        md5_1 = hashlib.md5(file(DB_FILE,"r").read())
        self.assertNotEqual(md5_0, md5_1)
