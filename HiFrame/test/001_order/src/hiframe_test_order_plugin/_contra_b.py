import hiframe

class T(hiframe.Plugin):

    def contra_b_a(self):
        pass
    
    def contra_b_b(self):
        pass
    
    contra_b_a.key_list=[{"id":"contra_b","order":2,"before":["hiframe_test_order_plugin.contra_b_b"]}]
    contra_b_b.key_list=[{"id":"contra_b","order":1}]
