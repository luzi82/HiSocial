#!/usr/bin/python

import sys
import webjsoncgi_config
sys.path.insert(0, webjsoncgi_config.CORE_PATH)
sys.path.insert(0, "../common")

from hs_command import hs_command
import cgi
import json
import os

print "Content-Type: text/plain; charset=utf-8"
print

form = cgi.FieldStorage()

def action():
    if(not form.has_key("PKG")):
        return hs_command.fail(reason="bad pkg")
    if(not form.has_key("CMD")):
        return hs_command.fail(reason="bad cmd")
    args = {}
    for k in form.keys():
        if(not isinstance(k, str)):continue
        if(k==""):continue
        if(k[:1]=="_"):continue
        if(k=="CMD"):continue
        if(k=="PKG"):continue
        if(k.startswith("env_")):continue
        if(k.startswith("file_")):
            v = form[k].file
            if not v:continue
            args[k] = v
        else:
            v = form[k].value
            if(not isinstance(v, str)):continue
            args[k] = v
    args["env_ip"] = cgi.escape(os.environ["REMOTE_ADDR"])
    return hs_command.call(form["PKG"].value, form["CMD"].value, args)

ret = action()

print json.dumps(ret)
