'''
@author: luzi82
'''

enable_trace = False
enable_debug = False
_trace_indent = ""

def trace(v):
    global enable_trace, _trace_indent
    if(not enable_trace):
        return
    print(_trace_indent + str(v))

def trace_up(v):
    global enable_trace,_trace_indent
    if(not enable_trace):
        return
    print(_trace_indent + v)
    _trace_indent+=" "

def trace_down(v):
    global enable_trace,_trace_indent
    if(not enable_trace):
        return
    _trace_indent = _trace_indent[0:len(_trace_indent) - 1]
    print(_trace_indent + v)

def debug(v):
    if(not enable_debug):
        return
    print(_trace_indent + str(v))
