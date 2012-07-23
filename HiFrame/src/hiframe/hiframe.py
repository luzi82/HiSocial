import os
from types import FunctionType
import shutil
import ConfigParser

class HiFrame:
    
    # _plugin_path_list
    _plugin_path_list = None
        
    # key_id - [] - {"call":*,"pkg":*,"func":*}
    _func_dict = None
    
    _data_path = None
    
    _running = False
    
    _conf_file = None
    
    _config = None
    
    def __init__(self, plugin_path_list, filename="_hiframe", data_path=None, conf_file=None):
        self._plugin_path_list = plugin_path_list
        self._func_dict = _scan_func(plugin_path_list, filename)
        self._data_path = data_path
        self._conf_file = conf_file
        
        if self._conf_file != None:
            self._config = ConfigParser.ConfigParser()
            self._config.read(self._conf_file)
        
    def call(self, key, args={}):
        if not key in self._func_dict:
            return []
        ret = []
        for t in self._func_dict[key]:
            tt = t["call"](**args)
            ret.append({"pkg":t["pkg"], "func":t["func"], "ret":tt})
        return ret

    def build(self):
        if self._data_path != None:
            if not os.path.exists(self._data_path):
                os.makedirs(self._data_path)
                self.call("HiFrame.build")

    def clean(self):
        self.stop() # auto stop
        if self._data_path != None:
            if os.path.exists(self._data_path):
                shutil.rmtree(self._data_path)
                self.call("HiFrame.clean")

    def start(self):
        self.build() # auto build
        if not self._running:
            self.call("HiFrame.start")
            self._running = True

    def stop(self):
        if self._running:
            self.call("HiFrame.stop")
            self._running = False
            
    def get_config(self):
        return self._config

def _scan_func(plugin_path_list, filename):

    # key_id - key_order - [] - {"call":*,"pkg":*,"func":*}
    func_dict_0 = {}
    
    for plugin_path in plugin_path_list:
        for pkg_name in os.listdir(plugin_path):
            if(not os.path.isfile(plugin_path + "/" + pkg_name + "/" + filename + ".py")):continue
            m = __import__(name=pkg_name, fromlist=[filename])
            m = getattr(m, filename)
            m_attr_list = dir(m)
            for func_name in m_attr_list:
                func_call = getattr(m, func_name)
                if not isinstance(func_call, FunctionType): continue
                dir_f = dir(func_call)
                if not "key_list" in dir_f: continue
                key_list = func_call.key_list
                for key in key_list:
                    key_id = key["id"]
                    if "order" in key:
                        key_order = key["order"]
                    else:
                        key_order = 0
                    if not key_id in func_dict_0:
                        func_dict_0[key_id] = {}
                    tmp = func_dict_0[key_id]
                    if not key_order in tmp:
                        tmp[key_order] = []
                    tmp = tmp[key_order]
                    tmp.append({"call":func_call, "pkg":pkg_name, "func":func_name})
                    
    # key_id - [] - {"call":*,"pkg":*,"func":*}
    func_dict_1 = {}

    for key, v in func_dict_0.iteritems():
        t = []
        order_list = v.keys()
        order_list.sort()
        for order in order_list:
            t.extend(v[order])
        func_dict_1[key] = t

    return func_dict_1
