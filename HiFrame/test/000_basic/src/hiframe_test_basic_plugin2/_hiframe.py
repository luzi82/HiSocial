import hiframe

class HiframeTestBasicPlugin2(hiframe.Plugin):
    
    def pkg2_b(self):
        return "b"
    pkg2_b.key_list=[{"id":"pkg2","order":1}]
