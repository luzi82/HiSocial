import os
from types import FunctionType

class HiFrame:
    
    # _plugin_path_list
    _plugin_path_list=None
        
    # key_id - key_order - [] - {"func":*,"pkg":*}
    _func_dict=None
    
    def __init__(self,plugin_path_list):
        self._plugin_path_list=plugin_path_list
        self._func_dict=_scan_func(plugin_path_list)
        
    def call(self,key,args={}):
        if not key in self._func_dict:
            return []
        ret=[]
        order_list = self._func_dict[key].keys()
        order_list.sort()
        for t in order_list:
            tt = self._func_dict[key][t]
            for ttt in tt:
                tttt = ttt["call"](**args)
                ret.append({"pkg":ttt["pkg"],"func":ttt["func"],"ret":tttt})
        return ret

def _scan_func(plugin_path_list):
    func_dict={}
    
    for plugin_path in plugin_path_list:
        for pkg_name in os.listdir(plugin_path):
            if(not os.path.isfile(plugin_path+"/"+pkg_name+"/_hiframe.py")):continue
            m=__import__(name=pkg_name,fromlist=["_hiframe"])
            m_attr_list=dir(m._hiframe)
            for func_name in m_attr_list:
                func_call = getattr(m._hiframe,func_name)
                if not isinstance(func_call,FunctionType): continue
                dir_f = dir(func_call)
                if not "key_list" in dir_f: continue
                key_list = func_call.key_list
                for key in key_list:
                    key_id = key["id"]
                    if "order" in key:
                        key_order = key["order"]
                    else:
                        key_order = 0
                    if not key_id in func_dict:
                        func_dict[key_id]={}
                    tmp = func_dict[key_id]
                    if not key_order in tmp:
                        tmp[key_order] = []
                    tmp = tmp[key_order]
                    tmp.append({"call":func_call,"pkg":pkg_name,"func":func_name})

    return func_dict
