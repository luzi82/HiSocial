from base import Command
import _testcommon

class TestWebBasic(_testcommon.HsTest):
    
    def test_ping(self):
        data=self.call_web({'PKG': "base", 'CMD': "guest_ping", 'txt_value': "0000ffff"})
        self.assertEqual(data[Command.RESULT_KEY], Command.RESULT_VALUE_OK_TXT)
        self.assertEqual(data["value"], "ffff0000")

    def test_helloworld(self):
        data=self.call_web({'PKG': "test", 'CMD': "helloworld"})
        self.assertEqual(data[Command.RESULT_KEY], Command.RESULT_VALUE_OK_TXT)
        self.assertEqual(data["value"], "helloworld")

    def test_uppercase(self):
        data=self.call_web({'PKG': "test", 'CMD': "uppercase", "txt_a":"asdf"})
        self.assertEqual(data[Command.RESULT_KEY], Command.RESULT_VALUE_OK_TXT)
        self.assertEqual(data["value"], "ASDF")

