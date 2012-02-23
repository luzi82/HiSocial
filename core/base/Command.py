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
    except:
        return BAD_CALL
    ret = f(**args)
    if(ret == None):return NOT_IMPLEMENTED
    return ret

def list_cmd():
    '''
    list all pkg and cmd
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
            mv[attr[7:]]=inspect.getargspec(f).args
        if(len(mv)>0):ret[pkg]=mv
    return ret
                

def ok(result=None):
    global RESULT_OK
    return _merge_dict(RESULT_OK, result)

def fail(result=None, reason=None):
    global RESULT_FAIL
    ret = _merge_dict(RESULT_FAIL, result)
    if(reason != None):
        ret[FAIL_REASON_KEY] = reason
    return ret

def _merge_dict(a, b):
    ret = a.copy()
    if(b != None):ret.update(b)
    return ret

def _is_call_name(v):
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
