import hiframe

class HiframeTestBasicPlugin(hiframe.Plugin):
    
    def simple_func(self):
        return "simple ret"
    simple_func.key_list=[{"id":"simple"}]
    
    def simple_arg_func(self,abc):
        return abc+1
    simple_arg_func.key_list=[{"id":"simple_arg"}]
    
    def order_a(self):
        return "a"
    order_a.key_list=[{"id":"order"}]
    
    def order_b(self):
        return "b"
    order_b.key_list=[{"id":"order","order":1}]
    
    def order_c(self):
        return "c"
    order_c.key_list=[{"id":"order","order":-1}]
    
    def pkg2_a(self):
        return "a"
    pkg2_a.key_list=[{"id":"pkg2","order":100}]
    
    def pkg2_c(self):
        return "c"
    pkg2_c.key_list=[{"id":"pkg2","order":0}]
    
    def no_order_a(self):
        return "a"
    no_order_a.key_list=[{"id":"no_order"}]
    
    def no_order_b(self):
        return "b"
    no_order_b.key_list=[{"id":"no_order"}]
