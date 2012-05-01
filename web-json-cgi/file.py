#!/usr/bin/python

import sys
import webjsoncgi_config
import mimetypes
sys.path.insert(0, webjsoncgi_config.CORE_PATH)

from base import Command
import cgi
import os

form = cgi.FieldStorage()

def action():
    if(not form.has_key("PKG")):
        return None
    if(not form.has_key("CMD")):
        return None
    args = {}
    for k in form.keys():
        if(not isinstance(k, str)):continue
        if(k==""):continue
        if(k[:1]=="_"):continue
        if(k=="CMD"):continue
        if(k=="PKG"):continue
        v = form[k].value
        if(not isinstance(v, str)):continue
        args[k] = v
    args["_ip"] = cgi.escape(os.environ["REMOTE_ADDR"])
    return Command.get_file(form["PKG"].value, form["CMD"].value, args)

ret = action()

def output_error():
    print "Status: 400"
    print "Content-Type: text/plain; charset=utf-8"
    print

if((ret==None) or (ret[Command.RESULT_KEY]!=Command.RESULT_VALUE_OK_TXT)):
    output_error();
elif(ret["file_type"]=="local"):
    filename=ret.has_key("file_name")
    if(ret.has_key("mime")):
        mime=ret["mime"]
    else:
        tmp=mimetypes.guess_type(filename)
        if(tmp[1]!=None):
            mime="%(type); charset=$(encoding)"%{"type":tmp[0],"encoding":tmp[1]}
        else:
            mime="%(type)"%{"type":tmp[0]}
    # Should add expire info/check?
    print "Status: 200"
    print "Content-Type: %(mime)"%{"mime":mime}
    print
    pass
elif(ret["file_type"]=="buffer"):
    pass
else:
    output_error();
