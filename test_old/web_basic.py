from hs_plugin import hs_plugin
import _testcommon
from base import Runtime
from admin import reset
import core_config
from hs_common.hs_cleanup import Cleanup

class TestWebBasic(_testcommon.HsTest):
    
    def setUp(self):
        Runtime.enable_trace = False
        reset.reset(_testcommon)
        Runtime.enable_trace = True

    def test_ping(self):
        data=self.call_web_json({'PKG': "base", 'CMD': "guest_ping", 'txt_value': "0000ffff"})
        self.check_ok(data)
        self.assertEqual(data["value"], "ffff0000")

    def test_helloworld(self):
        data=self.call_web_json({'PKG': "test", 'CMD': "helloworld", "test": core_config.TEST_KEY})
        self.check_ok(data)
        self.assertEqual(data["value"], "helloworld")

    def test_uppercase(self):
        data=self.call_web_json({'PKG': "test", 'CMD': "uppercase", "txt_a":"asdf", "test": core_config.TEST_KEY})
        self.check_ok(data)
        self.assertEqual(data["value"], "ASDF")

    def test_nokey(self):
        data=self.call_web_json({'PKG': "test", 'CMD': "helloworld"})
        self.check_fail(data)

    def test_file(self):
        output_name,data=self.call_web_raw({'PKG': "test", 'CMD': "hellofile", "test": core_config.TEST_KEY})
        self.assertEqual(output_name,"test.txt")
        fo = open("res/test0.torrent.txt")
        d = fo.read()
        fo.close()
        self.assertEqual(data,d)

    def test_file2(self):
        output_name,data=self.call_web_raw({'PKG': "test", 'CMD': "hellofile2", "test": core_config.TEST_KEY})
        self.assertEqual(output_name,"test.txt")
        fo = open("res/test0.torrent.txt")
        d = fo.read()
        fo.close()
        self.assertEqual(data,d)

    def test_fileimage(self):
        output_name,data=self.call_web_raw({'PKG': "test", 'CMD': "helloimage", "test": core_config.TEST_KEY})
        self.assertEqual(output_name,"test.png")
        fo = open("res/math0.png")
        d = fo.read()
        fo.close()
        self.assertEqual(data,d)

    def test_upload(self):
        cleanup = Cleanup()
        f = open("res/math0.png")
        cleanup.push(f.close)
        data=self.call_web_json_ok({'PKG': "test", 'CMD': "file_md5sum", "file_v": f, "test": core_config.TEST_KEY})
        cleanup.clean_all()
        self.assertEqual(data[hs_plugin.VALUE_KEY], "953f955591ac68da817cf66972e79d60")
