from base import Command
import _testfunc

class TestWebBasic(_testfunc.TestFunc):
    
    def test_ping(self):
        data=self.call_web({'PKG': "base", 'CMD': "guest_ping", 'txt_value': "0000ffff"})
        self.assertEqual(data[Command.RESULT_KEY], Command.RESULT_VALUE_OK_TXT)
        self.assertEqual(data["value"], "ffff0000")
