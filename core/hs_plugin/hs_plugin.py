from base.Runtime import debug
from types import FunctionType
import os
import string
import inspect
import core_config
import sys
import traceback
import pprint

RESULT_KEY = "result"
RESULT_VALUE_FAIL_TXT = "fail"
RESULT_VALUE_OK_TXT = "ok"

FAIL_REASON_KEY = "fail_reason"

RESULT_FAIL = {RESULT_KEY:RESULT_VALUE_FAIL_TXT}
RESULT_OK = {RESULT_KEY:RESULT_VALUE_OK_TXT}

VALUE_KEY = "value"

def call(package, func_name, args={}):
    return _call("command", package, func_name, args)

def get_file(package, func_name, args={}):
    return _call("file", package, func_name, args)

def list_cmd():
    '''
    list all pkg and cmd
    
    @rtype:  dict
    @return: a muliple layer dict, (package-name) -> (function-name) -> [arg list]
    '''
    me=os.path.abspath(__file__)
    core_path=os.path.dirname(os.path.dirname(me))
    ret={}
    for pkg in os.listdir(core_path):
        if(not os.path.isfile(core_path+"/"+pkg+"/_hisocial.py")):continue
        m=__import__(name=pkg,fromlist=["_hisocial"])
        attr_list=dir(m._hisocial)
        mv={}
        for attr in attr_list:
            if not attr.startswith("command_"): continue
            f = getattr(m._hisocial,attr)
            if not isinstance(f,FunctionType): continue
            av = inspect.getargspec(f).args
            avv = []
            for k in av :
                if k.startswith("env_") :
                    continue 
                avv.append(k)
            mv[attr[8:]] = avv
        if(len(mv)>0):ret[pkg]=mv
    return ret
                

def ok(result=None, value=None):
    '''
    Create a OK command return
    
    @type  result: dict
    @param result: dict key-value add to return value
    @type  value: str
    @param value: return value
    
    @rtype:  dict
    @return: A OK command return
    '''
    global RESULT_OK
    ret = _merge_dict(RESULT_OK, result)
    if(value != None):
        ret[VALUE_KEY] = value
    return ret

def fail(result=None, reason=None):
    '''
    Create a FAIL command return
    
    @type  result: dict
    @param result: dict key-value add to return value
    @type  reason: str
    @param reason: fail reason
    
    @rtype:  dict
    @return: A FAIL command return
    '''
    global RESULT_FAIL
    ret = _merge_dict(RESULT_FAIL, result)
    if(reason != None):
        ret[FAIL_REASON_KEY] = reason
    return ret

def _call(prefix, package, func_name, args={}):
    try:
        if(not _is_call_name(package)):
            debug("not _is_call_name(package)")
            return BAD_CALL
        if(not _is_call_name(func_name)):
            debug("not _is_call_name(func_name)")
            return BAD_CALL
        if(not isinstance(args, dict)):
            debug("not isinstance(args, dict)")
            return BAD_CALL
        if(_check_test(args)==False):
            debug("_check_test(args)==False")
            return BAD_CALL
        mm = __import__(name=package, fromlist=["_hisocial"])
        f = getattr(mm._hisocial, prefix+"_"+func_name)
        if(not isinstance(f, FunctionType)):
            return BAD_CALL
        if(f.__module__ != package + "._hisocial"):
            return BAD_CALL
        av = inspect.getargspec(f).args
#        args0 = dict((k,args[k])for k in av)
        args0={}
        for key in av:
            if key.startswith("txt_"):
                args0[key]=args[key]
            elif key.startswith("env_"):
                args0[key]=args[key]
            elif key.startswith("file_"):
                args0[key]=args[key]
            elif key.startswith("txtf_"):
                m = _convert_arg(key,args[key],args)
                if(m[RESULT_KEY]==RESULT_VALUE_OK_TXT):
                    args0[key]=m[VALUE_KEY]
                else:
                    return m
            else:
                return BAD_API
        ret = f(**args0)
        if(ret == None):return NOT_IMPLEMENTED
        return ret
    except Exception as e:
        return _unknown_err(e)

def _check_test(args):
    if(core_config.TEST_KEY==None):
        return None
    if(core_config.TEST_KEY==""):
        return None
    if(not ("test" in args)):
        return None
    if args["test"] != core_config.TEST_KEY:
        return False
    me=os.path.abspath(__file__)
    hisocial_root_path=os.path.dirname(os.path.dirname(os.path.dirname(me)))
    sys.path.insert(0, hisocial_root_path+"/test")
    return True

def _convert_arg(key,value,args):
    try:
        kk = key.rsplit("_")
        if(len(kk)<3):
            return BAD_API
        package=kk[1]
        func_name=kk[2]
        if(not _is_call_name(package)):
            debug("not _is_call_name(package)")
            return BAD_CALL
        if(not _is_call_name(func_name)):
            debug("not _is_call_name(func_name)")
            return BAD_CALL
        mm = __import__(name=package, fromlist=["_hisocial"])
        f = getattr(mm._hisocial, "argfilter_"+func_name)
        if(not isinstance(f, FunctionType)):
            return BAD_CALL
        if(f.__module__ != package + "._hisocial"):
            return BAD_CALL
        av = inspect.getargspec(f).args
        args0={}
        args0["v"]=value
        for key in av:
            if key.startswith("env_"):
                args0[key]=args[key]
        ret = f(**args0)
        if(ret == None):return NOT_IMPLEMENTED
        return ret
    except:
        return _unknown_err()

def _merge_dict(a, b):
    '''
    Combine two dict
    
    @type a: dict
    @type b: dict, have priority
    
    @rtype:  dict
    @return: combined dict
    '''
    ret = a.copy()
    if(b != None):ret.update(b)
    return ret

def _is_call_name(v):
    '''
    Check if a str is valid package/func name.
    
    @type v: str
    
    @rtype:  boolean
    @return: True iff str is valid package/func name
    '''
    r = string.ascii_letters + string.digits + "_"
    if(v == None):return False
    if(not isinstance(v, str)):return False
    if(len(v) <= 0):return False
    if(v[0] not in string.ascii_letters):return False
    for c in v :
        if(c not in r):return False
    return True

BAD_CALL = fail(reason="bad call")
BAD_API = fail(reason="bad api")
NOT_IMPLEMENTED = fail(reason="not implemented")
#UNKNOWN_ERR = fail(reason="unknown err")

def _unknown_err(ex = None):
    if core_config.TEST_KEY:
        f = traceback.extract_stack(limit=2)
        xfile, xline, xfunc, xtext = f[0]
        if ex == None:
            return fail(reason="ERR %s %d"%(xfile,xline))
        else:
            return fail(reason="ERR %s %d %s"%(xfile,xline,pprint.pformat(ex)))
    else:
        return fail(reason="unknown err")
