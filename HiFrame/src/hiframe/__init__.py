import os
import shutil
import ConfigParser
import types
import copy

CONF_KEY = "HiFrame"

class HiFrame:
    
    # _plugin_info_DD : pkg - {module,class,obj}
    
    # _call_info_DVD : call_key - [order] - {call,pkg,module,class,func,obj}
    
    # plugin_D : pkg

    def __init__(self, plugin_path_list, filename_list=["_hiframe"], conf_file=None):
        self._plugin_path_list = plugin_path_list
        self._plugin_info_DD = _scan_plugin(self._plugin_path_list, filename_list, self)
        self._call_info_DVD = _scan_func(self._plugin_info_DD)
        self._data_path = None
        self._running = False
        self._conf_file = conf_file
        self._config = None

        self.plugin_D = {}
        for pkg_name,v in self._plugin_info_DD.iteritems():
            self.plugin_D[pkg_name]=v["obj"]
        
        if self._conf_file != None:
            self._config = ConfigParser.ConfigParser()
            tmp=self._config.read(self._conf_file)
            if len(tmp)==0:
                raise IOError

        if self._config != None :
            if self._config.has_option(CONF_KEY,"data_path") :
                self._data_path = os.path.abspath(self._config.get(CONF_KEY,"data_path"))
        
    def call(self, key, args={}):
        if not key in self._call_info_DVD:
            return []
        ret = []
        for t in self._call_info_DVD[key]:
            tt = t["call"](**args)
            ret.append({
                "pkg":t["pkg"],
                "module":t["module"],
                "class":t["class"],
                "func":t["func"],
                "ret":tt
            })
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
    
    def get_data_path(self,plugin_key=None):
        if plugin_key == None:
            return self._data_path
        else:
            return self._data_path+"/"+plugin_key
        
    def get_func_list(self,key):
        if not key in self._call_info_DVD:
            return None
        ret = []
        for t in self._call_info_DVD[key]:
            tt={}
            for i in ["call","pkg","class","module","func"]:tt[i]=t[i]
            ret.append(tt)
        return ret
    

def _scan_plugin(plugin_path_list, filename_list, hf):
    
    # pkg - {module,class,obj}
    ret = {}
    
    for plugin_path in plugin_path_list:
        for pkg_name in os.listdir(plugin_path):
            for filename in filename_list:
                if(not os.path.isfile(plugin_path + "/" + pkg_name + "/" + filename + ".py")):continue
                m = __import__(name=pkg_name, fromlist=[filename])
                m = getattr(m, filename)
                m_attr_list = dir(m)
                for c_name in m_attr_list:
                    c = getattr(m, c_name)
                    if not isinstance(c, types.ClassType): continue
                    if not issubclass(c, Plugin):continue
                    obj = c(hf)
                    ret[pkg_name]={"module":filename,"class":c.__name__,"obj":obj}
                    
    
    return ret

def _scan_func(plugin_list):
    
    # call_key - key_order - [] - {call,pkg,module,class,func,obj}
    func_dict_0 = {}
    
    # call_key - after_func - [ before_func ]
    before_after = {}

    # call_key - set(before_after_key)    
    before_after_key_set = {}

    # call_key - [] - {before,after,pkg,class,func,type}
    before_after_check = {}
    
    for pkg_name,plugin in plugin_list.iteritems(): #@UnusedVariable
        class_name=plugin["class"]
        o = plugin["obj"]
        c_attr_list = dir(o)
        for func_name in c_attr_list:
            func_call = getattr(o, func_name)
            if not isinstance(func_call, types.MethodType): continue
            dir_f = dir(func_call)
            if not "key_list" in dir_f: continue
            key_list = func_call.key_list
            for key in key_list:
                # TODO check if id exist, otherwise throw
                
                call_key = key["id"]
                
                if not isinstance(call_key,str):
                    raise BadFuncKeyValueException(None,pkg_name,class_name,func_name,"id")
                
                if "order" in key:
                    if not isinstance(key["order"],types.IntType):
                        raise BadFuncKeyValueException(call_key,pkg_name,class_name,func_name,"order")
                    key_order = key["order"]
                else:
                    key_order = 0

                if not call_key in func_dict_0:
                    func_dict_0[call_key] = {}
                tmp = func_dict_0[call_key]
                if not key_order in tmp:
                    tmp[key_order] = []
                tmp = tmp[key_order]
                
                tmp.append({
                    "call":func_call,
                    "pkg":pkg_name,
                    "module":plugin["module"],
                    "class":class_name,
                    "func":func_name,
                    "obj":plugin["obj"]
                })
                
                before_after_key = pkg_name+"."+func_name
                
                if not call_key in before_after_key_set:
                    before_after_key_set[call_key] = set()
                before_after_key_set[call_key].add(before_after_key)
                
                if not call_key in before_after_check:
                    before_after_check[call_key] = []
                
                if "after" in key:
                    if not isinstance(key["after"],list):
                        raise BadFuncKeyValueException(call_key,pkg_name,class_name,func_name,"after")
                    for tmp in key["after"]:
                        if not isinstance(tmp,str):
                            raise BadFuncKeyValueException(call_key,pkg_name,class_name,func_name,"after")
                        _before_after_link(before_after,call_key,tmp,before_after_key)
                        before_after_check[call_key].append({
                            "before":tmp,
                            "after":before_after_key,
                            "pkg":pkg_name,
                            "class":class_name,
                            "func":func_name,
                            "type":"after"
                        })

                if "before" in key:
                    if not isinstance(key["before"],list):
                        raise BadFuncKeyValueException(call_key,pkg_name,class_name,func_name,"before")
                    for tmp in key["before"]:
                        if not isinstance(tmp,str):
                            raise BadFuncKeyValueException(call_key,pkg_name,class_name,func_name,"before")
                        _before_after_link(before_after,call_key,before_after_key,tmp)
                        before_after_check[call_key].append({
                            "before":before_after_key,
                            "after":tmp,
                            "pkg":pkg_name,
                            "class":class_name,
                            "func":func_name,
                            "type":"before"
                        })

    # check before_after
    for bac_k, bac_v in before_after_check.iteritems():
        for bac_v_i in bac_v:
            if not bac_v_i["before"] in before_after_key_set[bac_k]:
                raise BadFuncKeyValueException(bac_k,bac_v_i["pkg"],bac_v_i["class"],bac_v_i["func"],bac_v_i["type"])
            if not bac_v_i["after"] in before_after_key_set[bac_k]:
                raise BadFuncKeyValueException(bac_k,bac_v_i["pkg"],bac_v_i["class"],bac_v_i["func"],bac_v_i["type"])
    
    # call_key - [order] - {call,pkg,module,class,func,obj}
    ret = {}

    for call_key, v in func_dict_0.iteritems():
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
                    if not _full_fill(before_after,call_key,func_done,before_after_key):
                        continue
                    t.append(entry)
                    v_order_done.append(before_after_key)
                    func_done.append(before_after_key)
                    have_add = True
                if not have_add:
                    raise BadFuncOrderException(call_key)
        ret[call_key] = t

    return ret

def _before_after_link(before_after,call_key,before_func,after_func):
    if call_key not in before_after:
        before_after[call_key] = {}
    tmp = before_after[call_key]
    
    if after_func not in tmp:
        tmp[after_func] = []
    tmp = tmp[after_func]
    
    tmp.append(before_func)

def _full_fill(before_after,call_key,func_done,after_func):
    if call_key not in before_after:
        return True
    tmp = before_after[call_key]
    
    if after_func not in tmp:
        return True
    tmp = tmp[after_func]
    
    for before_func in tmp:
        if before_func not in func_done:
            return False
    
    return True

class BadFuncOrderException(Exception):
    def __init__(self,call_key):
        self.call_key=call_key

class BadFuncKeyValueException(Exception):
    def __init__(self,call_key,pkg,class_name,func_name,bad_key):
        self.call_key=call_key
        self.pkg=pkg
        self.class_name=class_name
        self.func_name=func_name
        self.bad_key=bad_key

class Plugin:
    def __init__(self,hf):
        self.hiframe=hf # set by HiFrame later
