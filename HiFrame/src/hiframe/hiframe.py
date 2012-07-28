import os
from types import FunctionType
import shutil
import ConfigParser

CONF_KEY = "HiFrame"

class HiFrame:
    
    # _plugin_path_list
    _plugin_path_list = None
        
    # key_id - [] - {"call":*,"pkg":*,"func":*}
    _func_dict = None
    
    _data_path = None
    
    _running = False
    
    _conf_file = None
    
    _config = None
    
    def __init__(self, plugin_path_list, filename="_hiframe", conf_file=None):
        self._plugin_path_list = plugin_path_list
        self._func_dict = _scan_func(plugin_path_list, filename)
        self._conf_file = conf_file
        
        if self._conf_file != None:
            self._config = ConfigParser.ConfigParser()
            tmp=self._config.read(self._conf_file)
            if len(tmp)==0:
                raise IOError

        if self._config != None :
            if self._config.has_option(CONF_KEY,"data_path") :
                self._data_path = os.path.abspath(self._config.get(CONF_KEY,"data_path"))
        
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
                self.call("HiFrame.build",args={"frame":self})

    def clean(self):
        self.stop() # auto stop
        if self._data_path != None:
            if os.path.exists(self._data_path):
                shutil.rmtree(self._data_path)
                self.call("HiFrame.clean",args={"frame":self})

    def start(self):
        self.build() # auto build
        if not self._running:
            self.call("HiFrame.start",args={"frame":self})
            self._running = True

    def stop(self):
        if self._running:
            self.call("HiFrame.stop",args={"frame":self})
            self._running = False
            
    def get_config(self):
        return self._config
    
    def get_data_path(self,plugin_key=None):
        if plugin_key == None:
            return self._data_path
        else:
            return self._data_path+"/"+plugin_key

def _scan_func(plugin_path_list, filename):

    # key_id - key_order - [] - {"call":*,"pkg":*,"func":*}
    func_dict_0 = {}
    
    # key_id - after_func - [ before_func ]
    before_after = {}
    
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
                    
                    if not isinstance(key_id,str):
                        raise BadFuncKeyException
                    
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
                    
                    before_after_key = pkg_name+"."+func_name
                    
                    if "after" in key:
                        for tmp in key["after"]:
                            _before_after_link(before_after,key_id,tmp,before_after_key)

                    if "before" in key:
                        for tmp in key["before"]:
                            _before_after_link(before_after,key_id,before_after_key,tmp)

    # key_id - [] - {"call":*,"pkg":*,"func":*}
    func_dict_1 = {}

    for key, v in func_dict_0.iteritems():
        func_done = []
        t = []
        order_list = v.keys()
        order_list.sort()
        for order in order_list:
            v_order = v[order]
            v_order_done = []
            while len(v_order_done) != len(v_order):
                have_add = False
                for entry in v_order:
                    before_after_key = entry["pkg"]+"."+entry["func"]
                    if before_after_key in v_order_done:
                        continue
                    if not _full_fill(before_after,key,func_done,before_after_key):
                        continue
                    t.append(entry)
                    v_order_done.append(before_after_key)
                    func_done.append(before_after_key)
                    have_add = True
                if not have_add:
                    raise BadFuncKeyException
        func_dict_1[key] = t

    return func_dict_1

def _before_after_link(before_after,key_id,before_func,after_func):
    if key_id not in before_after:
        before_after[key_id] = {}
    tmp = before_after[key_id]
    
    if after_func not in tmp:
        tmp[after_func] = []
    tmp = tmp[after_func]
    
    tmp.append(before_func)

def _full_fill(before_after,key_id,func_done,after_func):
    if key_id not in before_after:
        return True
    tmp = before_after[key_id]
    
    if after_func not in tmp:
        return True
    tmp = tmp[after_func]
    
    for before_func in tmp:
        if before_func not in func_done:
            return False
    
    return True

class BadFuncKeyException(Exception):
    pass
