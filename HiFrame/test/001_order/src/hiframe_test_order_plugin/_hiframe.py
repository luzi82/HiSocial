import hiframe

class T(hiframe.Plugin):

    ###################
    
    def after_abc_aaa(self):
        pass
    
    def after_abc_bbb(self):
        pass
    
    def after_abc_ccc(self):
        pass
    
    after_abc_aaa.key_list=[{"id":"after_abc"}]
    after_abc_bbb.key_list=[{"id":"after_abc","after":["hiframe_test_order_plugin.after_abc_aaa"]}]
    after_abc_ccc.key_list=[{"id":"after_abc","after":["hiframe_test_order_plugin.after_abc_bbb"]}]
    
    ###################
    
    def after_cba_aaa(self):
        pass
    
    def after_cba_bbb(self):
        pass
    
    def after_cba_ccc(self):
        pass
    
    after_cba_aaa.key_list=[{"id":"after_cba","after":["hiframe_test_order_plugin.after_cba_bbb"]}]
    after_cba_bbb.key_list=[{"id":"after_cba","after":["hiframe_test_order_plugin.after_cba_ccc"]}]
    after_cba_ccc.key_list=[{"id":"after_cba"}]
    
    ###################
    
    def after2_aaa(self):
        pass
    
    def after2_bbb(self):
        pass
    
    def after2_ccc(self):
        pass
    
    after2_aaa.key_list=[{"id":"after2"}]
    after2_bbb.key_list=[{"id":"after2","after":["hiframe_test_order_plugin.after2_aaa","hiframe_test_order_plugin.after2_ccc"]}]
    after2_ccc.key_list=[{"id":"after2"}]
    
    ###################
    
    def before_abc_aaa(self):
        pass
    
    def before_abc_bbb(self):
        pass
    
    def before_abc_ccc(self):
        pass
    
    before_abc_aaa.key_list=[{"id":"before_abc","before":["hiframe_test_order_plugin.before_abc_bbb"]}]
    before_abc_bbb.key_list=[{"id":"before_abc","before":["hiframe_test_order_plugin.before_abc_ccc"]}]
    before_abc_ccc.key_list=[{"id":"before_abc"}]
    
    ###################
    
    def before_cba_aaa(self):
        pass
    
    def before_cba_bbb(self):
        pass
    
    def before_cba_ccc(self):
        pass
    
    before_cba_aaa.key_list=[{"id":"before_cba"}]
    before_cba_bbb.key_list=[{"id":"before_cba","before":["hiframe_test_order_plugin.before_cba_aaa"]}]
    before_cba_ccc.key_list=[{"id":"before_cba","before":["hiframe_test_order_plugin.before_cba_bbb"]}]
    
    ###################
    
    def before2_aaa(self):
        pass
    
    def before2_bbb(self):
        pass
    
    def before2_ccc(self):
        pass
    
    before2_aaa.key_list=[{"id":"before2"}]
    before2_bbb.key_list=[{"id":"before2","before":["hiframe_test_order_plugin.before2_aaa","hiframe_test_order_plugin.before2_ccc"]}]
    before2_ccc.key_list=[{"id":"before2"}]
    
    ###################
    
    def afterbefore_abc_aaa(self):
        pass
    
    def afterbefore_abc_bbb(self):
        pass
    
    def afterbefore_abc_ccc(self):
        pass
    
    afterbefore_abc_aaa.key_list=[{"id":"afterbefore_abc"}]
    afterbefore_abc_bbb.key_list=[{"id":"afterbefore_abc","after":["hiframe_test_order_plugin.afterbefore_abc_aaa"],"before":["hiframe_test_order_plugin.afterbefore_abc_ccc"]}]
    afterbefore_abc_ccc.key_list=[{"id":"afterbefore_abc"}]
    
    ###################
    
    def afterbefore_cba_aaa(self):
        pass
    
    def afterbefore_cba_bbb(self):
        pass
    
    def afterbefore_cba_ccc(self):
        pass
    
    afterbefore_cba_aaa.key_list=[{"id":"afterbefore_cba"}]
    afterbefore_cba_bbb.key_list=[{"id":"afterbefore_cba","after":["hiframe_test_order_plugin.afterbefore_cba_ccc"],"before":["hiframe_test_order_plugin.afterbefore_cba_aaa"]}]
    afterbefore_cba_ccc.key_list=[{"id":"afterbefore_cba"}]
    
    ###################
    
    def order_afterbefore_mix_cba_ccc(self):
        pass
    def order_afterbefore_mix_cba_aaa(self):
        pass
    def order_afterbefore_mix_cba_bbb(self):
        pass
    
    order_afterbefore_mix_cba_aaa.key_list=[{"id":"order_afterbefore_mix_cba","order":2}]
    order_afterbefore_mix_cba_bbb.key_list=[{"id":"order_afterbefore_mix_cba","order":1}]
    order_afterbefore_mix_cba_ccc.key_list=[{"id":"order_afterbefore_mix_cba","before":["hiframe_test_order_plugin.order_afterbefore_mix_cba_bbb"]}]
    
    ###################
    
    def together_ba_aaa(self):
        pass
    def together_ba_bbb(self):
        pass
    
    together_ba_aaa.key_list=[{"id":"together_ba","after":["hiframe_test_order_plugin.together_ba_bbb"]}]
    together_ba_bbb.key_list=[{"id":"together_ba","before":["hiframe_test_order_plugin.together_ba_aaa"]}]
