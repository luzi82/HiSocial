from base import Command
import base
#import pprint
import unittest

class TestCommand(unittest.TestCase):
    
    def test_guest_ping_pass(self):
        cv = [["00000000", "ffffffff"],
              ["00000001", "fffffffe"],
              ["a7845763", "587ba89c"],
              ["8da581bf", "725a7e40"],
              ["0da581bf", "f25a7e40"]
             ]
        for c in cv :
            r = Command.call("base", "guest_ping", {"txt_value":c[0].upper()})
            self.assertTrue(r != None)
            self.assertTrue(isinstance(r,dict))
            self.assertEqual(len(r), 2)
            self.assertEqual(r[Command.RESULT_KEY], Command.RESULT_VALUE_OK_TXT)
            self.assertEqual(r["value"],c[1].lower())
            r = Command.call("base", "guest_ping", {"txt_value":c[0].lower()})
            self.assertTrue(r != None)
            self.assertTrue(isinstance(r,dict))
            self.assertEqual(len(r), 2)
            self.assertEqual(r[Command.RESULT_KEY], Command.RESULT_VALUE_OK_TXT)
            self.assertEqual(r["value"],c[1].lower())
            r = Command.call("base", "guest_ping", {"txt_value":c[1].upper()})
            self.assertTrue(r != None)
            self.assertTrue(isinstance(r,dict))
            self.assertEqual(len(r), 2)
            self.assertEqual(r[Command.RESULT_KEY], Command.RESULT_VALUE_OK_TXT)
            self.assertEqual(r["value"],c[0].lower())
            r = Command.call("base", "guest_ping", {"txt_value":c[1].lower()})
            self.assertTrue(r != None)
            self.assertTrue(isinstance(r,dict))
            self.assertEqual(len(r), 2)
            self.assertEqual(r[Command.RESULT_KEY], Command.RESULT_VALUE_OK_TXT)
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
            r = Command.call("base", "guest_ping", {"txt_value":c})
            self.assertTrue(r != None)
            self.assertTrue(isinstance(r,dict))
            self.assertEqual(len(r), 2)
            self.assertEqual(r[Command.RESULT_KEY], Command.RESULT_VALUE_FAIL_TXT)
            self.assertEqual(r["fail_reason"],"bad value")

    def test_list_cmd(self):
        ret = base._command.command_guest_list_cmd()
        self.assertEqual(ret[base.Command.RESULT_KEY],base.Command.RESULT_VALUE_OK_TXT)
#        pprint.pprint(ret)
        self.assertTrue("value" in ret)
        self.assertTrue("base" in ret["value"])
        self.assertTrue("guest_list_cmd" in ret["value"]["base"])
        self.assertEqual(ret["value"]["base"]["guest_list_cmd"],[])

    def test_test_module(self):
        ret = Command.call("test","helloworld")
        self.assertTrue(ret != None)
        self.assertTrue(isinstance(ret,dict))
        self.assertEqual(ret[Command.RESULT_KEY], Command.RESULT_VALUE_OK_TXT)
        self.assertEqual(ret["value"], "helloworld")

    def test_arg(self):
        ret = Command.call("test","uppercase",{"txt_a":"asdf"})
        self.assertTrue(ret != None)
        self.assertTrue(isinstance(ret,dict))
        self.assertEqual(ret[Command.RESULT_KEY], Command.RESULT_VALUE_OK_TXT)
        self.assertEqual(ret["value"], "ASDF")

    def test_arg_filter(self):
        ret = Command.call("test","uppercase_arg",{"txtf_test_upper":"qwer"})
        self.assertTrue(ret != None)
        self.assertTrue(isinstance(ret,dict))
        self.assertEqual(ret[Command.RESULT_KEY], Command.RESULT_VALUE_OK_TXT)
        self.assertEqual(ret["value"], "QWER")
