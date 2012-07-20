import hs_plugin.hs_plugin
import hs_plugin._hisocial
import _testcommon

class TestCommand(_testcommon.HsTest):
    
    def test_guest_ping_pass(self):
        cv = [["00000000", "ffffffff"],
              ["00000001", "fffffffe"],
              ["a7845763", "587ba89c"],
              ["8da581bf", "725a7e40"],
              ["0da581bf", "f25a7e40"]
             ]
        for c in cv :
            r = hs_plugin.hs_plugin.call("base", "guest_ping", {"txt_value":c[0].upper()})
            self.check_ok(r)
            self.assertEqual(len(r), 2)
            self.assertEqual(r["value"],c[1].lower())
            r = hs_plugin.hs_plugin.call("base", "guest_ping", {"txt_value":c[0].lower()})
            self.check_ok(r)
            self.assertEqual(len(r), 2)
            self.assertEqual(r["value"],c[1].lower())
            r = hs_plugin.hs_plugin.call("base", "guest_ping", {"txt_value":c[1].upper()})
            self.check_ok(r)
            self.assertEqual(len(r), 2)
            self.assertEqual(r["value"],c[0].lower())
            r = hs_plugin.hs_plugin.call("base", "guest_ping", {"txt_value":c[1].lower()})
            self.check_ok(r)
            self.assertEqual(len(r), 2)
            self.assertEqual(r["value"],c[0].lower())

    def test_guest_ping_fail(self):
        cv = ["asdf",
              "0000",
              "1234",
              "dddd",
              "1234567890",
              "-9999999",
              "-99999999",
              "9999999",
              "999999999"
             ]
        for c in cv :
            r = hs_plugin.hs_plugin.call("base", "guest_ping", {"txt_value":c})
            self.assertTrue(r != None)
            self.assertTrue(isinstance(r,dict))
            self.assertEqual(len(r), 2)
            self.assertEqual(r[hs_plugin.hs_plugin.RESULT_KEY], hs_plugin.hs_plugin.RESULT_VALUE_FAIL_TXT)
            self.assertEqual(r["fail_reason"],"bad value")

    def test_list_cmd(self):
        ret = hs_plugin._hisocial.command_guest_list_cmd()
        self.check_ok(ret)
        self.assertTrue("value" in ret)
        self.assertTrue("hs_plugin" in ret["value"])
        self.assertTrue("guest_list_cmd" in ret["value"]["hs_plugin"])
        self.assertEqual(ret["value"]["hs_plugin"]["guest_list_cmd"],[])

    def test_test_module(self):
        ret = hs_plugin.hs_plugin.call("test","helloworld")
        self.check_ok(ret)
        self.assertEqual(ret["value"], "helloworld")

    def test_arg(self):
        ret = hs_plugin.hs_plugin.call("test","uppercase",{"txt_a":"asdf"})
        self.check_ok(ret)
        self.assertEqual(ret["value"], "ASDF")

    def test_arg_filter(self):
        ret = hs_plugin.hs_plugin.call("test","uppercase_arg",{"txtf_test_upper":"qwer"})
        self.check_ok(ret)
        self.assertEqual(ret["value"], "QWER")

    def test_hellofile(self):
        ret = hs_plugin.hs_plugin.get_file("test","hellofile")
        self.check_ok(ret)
        self.assertEqual(ret["file_type"], "local")
        self.assertEqual(ret["mime"], "text/plain; charset=us-ascii")
        self.assertTrue(ret["file_name"].endswith("/test/res/test0.torrent.txt"))

    def test_hellofile2(self):
        ret = hs_plugin.hs_plugin.get_file("test","hellofile2")
        self.check_ok(ret)
        self.assertEqual(ret["file_type"], "local")
        self.assertTrue(not ("mime" in ret))
        self.assertTrue(ret["file_name"].endswith("/test/res/test0.torrent.txt"))
