import hiframe

class HiframeTestBasicPlugin_ABC(hiframe.Plugin):
    
    def abc_func(self):
        return "abc ret"
    abc_func.key_list=[{"id":"abc key"}]
