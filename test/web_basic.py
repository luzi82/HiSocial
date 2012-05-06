from base import Command
import _testcommon
from base import Runtime
from admin import reset
import core_config

class TestWebBasic(_testcommon.HsTest):
    
    def setUp(self):
        Runtime.enable_trace = False
        reset.reset(_testcommon)
        Runtime.enable_trace = True

    def test_ping(self):
        data=self.call_web({'PKG': "base", 'CMD': "guest_ping", 'txt_value': "0000ffff"})
        self.assertEqual(data[Command.RESULT_KEY], Command.RESULT_VALUE_OK_TXT)
        self.assertEqual(data["value"], "ffff0000")

    def test_helloworld(self):
        data=self.call_web({'PKG': "test", 'CMD': "helloworld", "test": core_config.TEST_KEY})
        self.assertEqual(data[Command.RESULT_KEY], Command.RESULT_VALUE_OK_TXT)
        self.assertEqual(data["value"], "helloworld")

    def test_uppercase(self):
        data=self.call_web({'PKG': "test", 'CMD': "uppercase", "txt_a":"asdf", "test": core_config.TEST_KEY})
        self.assertEqual(data[Command.RESULT_KEY], Command.RESULT_VALUE_OK_TXT)
        self.assertEqual(data["value"], "ASDF")

    def test_nokey(self):
        data=self.call_web({'PKG': "test", 'CMD': "helloworld"})
        self.assertEqual(data[Command.RESULT_KEY], Command.RESULT_VALUE_FAIL_TXT)
