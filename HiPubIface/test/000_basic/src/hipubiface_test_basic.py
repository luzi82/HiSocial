import unittest
import os
import hiframe
import hipubiface_test_basic_plugin._hiframe

MY_ABSOLUTE_PATH = os.path.abspath(__file__)
MY_ABSOLUTE_PARENT = os.path.dirname(MY_ABSOLUTE_PATH)

HIPUBIFACE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(MY_ABSOLUTE_PARENT)))
HIPUBIFACE_SRC_PATH = HIPUBIFACE_PATH+"/src"

class HipubifaceTestBasic(unittest.TestCase):
    
#    def test_guest_ping_pass(self):
#        cv = [["00000000", "ffffffff"],
#              ["00000001", "fffffffe"],
#              ["a7845763", "587ba89c"],
#              ["8da581bf", "725a7e40"],
#              ["0da581bf", "f25a7e40"]
#             ]
#        for c in cv :
#            r = hipubiface.call("base", "guest_ping", {"txt_value":c[0].upper()})
#            self.check_ok(r)
#            self.assertEqual(r["type"],"value")
#            self.assertEqual(r["value"],c[1].lower())
#            
#            r = hipubiface.call("base", "guest_ping", {"txt_value":c[0].lower()})
#            self.check_ok(r)
#            self.assertEqual(r["type"],"value")
#            self.assertEqual(r["value"],c[1].lower())
#            
#            r = hipubiface.call("base", "guest_ping", {"txt_value":c[1].upper()})
#            self.check_ok(r)
#            self.assertEqual(r["type"],"value")
#            self.assertEqual(r["value"],c[0].lower())
#            
#            r = hipubiface.call("base", "guest_ping", {"txt_value":c[1].lower()})
#            self.check_ok(r)
#            self.assertEqual(r["type"],"value")
#            self.assertEqual(r["value"],c[0].lower())
#
#    def test_guest_ping_fail(self):
#        cv = ["asdf",
#              "0000",
#              "1234",
#              "dddd",
#              "1234567890",
#              "-9999999",
#              "-99999999",
#              "9999999",
#              "999999999"
#             ]
#        for c in cv :
#            r = hipubiface.call("base", "guest_ping", {"txt_value":c})
#            self.assertTrue(r != None)
#            self.assertTrue(isinstance(r,dict))
#            self.assertEqual(r[hipubiface.RESULT_KEY], hipubiface.RESULT_VALUE_FAIL_TXT)
#            self.assertEqual(r["fail_reason"],"bad value")

#    def test_list_cmd(self):
#        ret = hipubiface._hiframe.command_guest_list_cmd()
#        self.check_ok(ret)
#        self.assertEqual(ret["type"],"value")
#        self.assertTrue("value" in ret)
#        self.assertTrue("hs_plugin" in ret["value"])
#        self.assertTrue("guest_list_cmd" in ret["value"]["hs_plugin"])
#        self.assertEqual(ret["value"]["hs_plugin"]["guest_list_cmd"],[])

    def test_call_noarg(self):
        hf=hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT,HIPUBIFACE_SRC_PATH])
        hf.start()
        
        me=hf.plugin_D["hipubiface"]
        
        ret = me.call("hipubiface_test_basic_plugin","helloworld")
        self.assertEqual(ret, "helloworld")

    def test_call_arg(self):
        hf=hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT,HIPUBIFACE_SRC_PATH])
        hf.start()

        me=hf.plugin_D["hipubiface"]
        
        ret = me.call("hipubiface_test_basic_plugin","uppercase",{"txt_a":"asdf"})
        self.assertEqual(ret, "ASDF")

    def test_call_exception(self):
        hf=hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT,HIPUBIFACE_SRC_PATH])
        hf.start()

        me=hf.plugin_D["hipubiface"]

        try:        
            me.call("hipubiface_test_basic_plugin","hello_exception")
            self.fail()
        except hipubiface_test_basic_plugin._hiframe.TestException:
            pass
        except:
            self.fail()

#    def test_hellofile(self):
#        ret = hipubiface.call("hipubiface_test_basic_plugin","hellofile")
#        self.check_ok(ret)
#        self.assertEqual(ret["type"], "file")
#        self.assertEqual(ret["file_type"], "local")
#        self.assertEqual(ret["mime"], "text/plain; charset=us-ascii")
#        self.assertTrue(ret["file_name"].endswith("/test/res/test0.torrent.txt"))
#
#    def test_hellofile2(self):
#        ret = hipubiface.call("hipubiface_test_basic_plugin","hellofile2")
#        self.check_ok(ret)
#        self.assertEqual(ret["type"], "file")
#        self.assertEqual(ret["file_type"], "local")
#        self.assertTrue(not ("mime" in ret))
#        self.assertTrue(ret["file_name"].endswith("/test/res/test0.torrent.txt"))
