import hiframe

class HiPubIface(hiframe.Plugin):
    
    # _func_info_DD : pkg_name,func_name - {obj,call} 
    
    def start(self):
        self._func_info_DD = {}
        func_info_DV = self.hiframe.get_func_list("HiPubIface.cmd")
        for func_info_D in func_info_DV:
            pkg_name=func_info_D["pkg"]
            func_name=func_info_D["func"]
            call=func_info_D["call"]
            obj=func_info_D["obj"]
            self._func_info_DD[pkg_name,func_name]={"obj":obj,"call":call}
    start.key_list=[{"id":"HiFrame.start"}]
    
    def stop(self):
        self._func_info_DD = None
    stop.key_list=[{"id":"HiFrame.stop"}]

    def call(self,pkg_name,func_name,arg_D={}):
        func_info_D = self._func_info_DD[pkg_name,func_name]
        func = func_info_D["call"]
        obj = func_info_D["obj"]

        ret = func(obj,**arg_D)

        return ret
