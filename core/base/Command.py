from base.Runtime import trace, debug
from types import FunctionType
import os
import string
import inspect
RESULT_KEY = "result"
RESULT_VALUE_FAIL_TXT = "fail"
RESULT_VALUE_OK_TXT = "ok"

FAIL_REASON_KEY = "fail_reason"

RESULT_FAIL = {RESULT_KEY:RESULT_VALUE_FAIL_TXT}
RESULT_OK = {RESULT_KEY:RESULT_VALUE_OK_TXT}

def call(package, func_name, args={}):
    """
    Call a command in a sub-package
    It will call (package)/_command.py public_(func_name)(args)
    
    @type  package: string
    @param package: package name
    @type  func_name: string
    @param func_name: function name
    @type  args: dict
    @param args: funtion arguments
    
    @rtype:  dict
    @return: command result
    """
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
        mm = __import__(name=package, fromlist=["_command"])
        f = getattr(mm._command, "public_"+func_name)
        if(not isinstance(f, FunctionType)):
            return BAD_CALL
        if(f.__module__ != package + "._command"):
            return BAD_CALL
        av = inspect.getargspec(f).args
        args0 = dict((k,args[k])for k in av)
        ret = f(**args0)
        if(ret == None):return NOT_IMPLEMENTED
        return ret
    except:
        return BAD_CALL

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
        if(not os.path.isfile(core_path+"/"+pkg+"/_command.py")):continue
        m=__import__(name=pkg,fromlist=["_command"])
        attr_list=dir(m._command)
        mv={}
        for attr in attr_list:
            if not attr.startswith("public_"): continue
            f = getattr(m._command,attr)
            if not isinstance(f,FunctionType): continue
            av = inspect.getargspec(f).args
            avv = []
            for k in av :
                if k[:1]!="_" : avv.append(k)
            mv[attr[7:]] = avv
        if(len(mv)>0):ret[pkg]=mv
    return ret
                

def ok(result=None):
    '''
    Create a OK command return
    
    @type  result: dict
    @param result: dict key-value add to return value
    
    @rtype:  dict
    @return: A OK command return
    '''
    global RESULT_OK
    return _merge_dict(RESULT_OK, result)

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
NOT_IMPLEMENTED = fail(reason="not implemented")
