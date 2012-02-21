from base import Command
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
            r = Command.call("base", "guest_ping", {"value":c[0].upper()})
            self.assertTrue(r != None)
            self.assertTrue(isinstance(r,dict))
            self.assertEqual(len(r), 2)
            self.assertEqual(r[Command.RESULT_KEY], Command.RESULT_VALUE_OK_TXT)
            self.assertEqual(r["value"],c[1].lower())
            r = Command.call("base", "guest_ping", {"value":c[0].lower()})
            self.assertTrue(r != None)
            self.assertTrue(isinstance(r,dict))
            self.assertEqual(len(r), 2)
            self.assertEqual(r[Command.RESULT_KEY], Command.RESULT_VALUE_OK_TXT)
            self.assertEqual(r["value"],c[1].lower())
            r = Command.call("base", "guest_ping", {"value":c[1].upper()})
            self.assertTrue(r != None)
            self.assertTrue(isinstance(r,dict))
            self.assertEqual(len(r), 2)
            self.assertEqual(r[Command.RESULT_KEY], Command.RESULT_VALUE_OK_TXT)
            self.assertEqual(r["value"],c[0].lower())
            r = Command.call("base", "guest_ping", {"value":c[1].lower()})
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
            r = Command.call("base", "guest_ping", {"value":c})
            self.assertTrue(r != None)
            self.assertTrue(isinstance(r,dict))
            self.assertEqual(len(r), 2)
            self.assertEqual(r[Command.RESULT_KEY], Command.RESULT_VALUE_FAIL_TXT)
            self.assertEqual(r["fail_reason"],"bad value")
