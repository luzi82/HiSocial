#!/usr/bin/python

import sys
import webjsoncgi_config
sys.path.insert(0, webjsoncgi_config.CORE_PATH)
sys.path.insert(0, "../common")

from base import Command
import cgi
import os
from hisocial.common import hs_mime

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
    args["env_ip"] = cgi.escape(os.environ["REMOTE_ADDR"])
    return Command.get_file(form["PKG"].value, form["CMD"].value, args)

ret = action()

def output_error():
    print "Status: 400"
    print "Content-Type: text/plain; charset=utf-8"
    print

if((ret==None) or (ret[Command.RESULT_KEY]!=Command.RESULT_VALUE_OK_TXT)):
    output_error();
elif(ret["file_type"]=="local"):
    filename=ret["file_name"]
    if(ret.has_key("mime")):
        mime=ret["mime"]
    else:
        mime=hs_mime.read_file(filename)
    # Should add expire info/check?
    print "Status: 200"
    print "Content-Type: %(mime)s"%{"mime":mime}
    if "output_name" in ret :
        print "Content-Disposition: attachment; filename=%(output_name)s"%ret
    print ""
    fo = open(filename,"rb")
    sys.stdout.write(fo.read())
    fo.close()
elif(ret["file_type"]=="buffer"):
    pass
else:
    output_error();
