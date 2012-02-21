'''
@author: luzi82
'''

from base.Runtime import trace, trace_down, trace_up
import os
#import inspect

def reset():
    module_list=[]
    me=os.path.abspath(__file__)
    module_to_name={}
#    trace ("me "+me)

    trace_up("Find module start")

    core_path=os.path.dirname(os.path.dirname(me))
#    trace ("core_path "+core_path)
    for i in os.listdir(core_path):
        if(os.path.isfile(core_path+"/"+i+"/_reset.py")):
            trace("Module found: "+i)
            m=__import__(name=i,fromlist=["_reset"])
            module_list.append(m._reset)
            module_to_name[m._reset]=i
    
    trace_down("done")
            
    trace_up("Clean start")
            
    clean_list={}
    for m in module_list:
        if(hasattr(m,"clean_order")&hasattr(m,"clean")):
#            trace(m.clean_order())
            clean_list[m.clean_order()]=m;
    for i in sorted(clean_list.keys()):
        m=clean_list[i]
        trace("Clean: "+module_to_name[m])
        m.clean()

    trace_down("done")
    
    trace_up("Build start")
        
    build_list={}
    for m in module_list:
        if(hasattr(m,"build_order")&hasattr(m,"build")):
#            trace(m.clean_order())
            build_list[m.build_order()]=m;
    for i in sorted(build_list.keys()):
        m=build_list[i]
        trace("Build: "+module_to_name[m])
        m.build()
        
    trace_down("done")
