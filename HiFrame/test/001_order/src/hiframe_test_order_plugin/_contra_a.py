import hiframe

class T(hiframe.Plugin):

    def contra_a_a(self):
        pass
    
    def contra_a_b(self):
        pass
    
    contra_a_a.key_list=[{"id":"contra_a","order":1,"after":["hiframe_test_order_plugin.contra_a_b"]}]
    contra_a_b.key_list=[{"id":"contra_a","order":2}]
