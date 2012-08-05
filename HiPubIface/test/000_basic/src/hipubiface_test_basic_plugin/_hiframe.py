import hipubiface
import hiframe

class T(hiframe.Plugin):

    def helloworld(self):
        return "helloworld"
    helloworld.key_list=[{"id":"HiPubIface.cmd"}]
    
    def uppercase(self,txt_a):
        return txt_a.upper()
    uppercase.key_list=[{"id":"HiPubIface.cmd"}]
    
    def hello_exception(self):
        raise TestException
    hello_exception.key_list=[{"id":"HiPubIface.cmd"}]

class TestException(Exception):
    pass
