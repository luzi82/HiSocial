import hiframe

class HiPubIface(hiframe.Plugin):
    
    # _func_D : pkg_name,func_name 
    
    def start(self):
        self._func_D = {}
        func_info_DV = self.hiframe.get_func_list("HiPubIface.cmd")
        for func_info_D in func_info_DV:
            pkg_name=func_info_D["pkg_name"]
            func_name=func_info_D["func_name"]
            func=func_info_D["func"]
            self._func_D[pkg_name,func_name]=func
    start.key_list=[{"id":"HiFrame.start"}]
    
    def stop(self):
        self._func_D = None
    stop.key_list=[{"id":"HiFrame.stop"}]

    def call(self,pkg_name,func_name,arg_D={}):
        func = self._func_D[pkg_name,func_name]

        ret = func(**arg_D)

        return ret
