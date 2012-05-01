#!/usr/bin/python

import sys
import webjsoncgi_config
sys.path.insert(0, webjsoncgi_config.CORE_PATH)

from base import Command
import cgi
import json
import os

print "Content-Type: text/plain; charset=utf-8"
print

form = cgi.FieldStorage()

def action():
    if(not form.has_key("PKG")):
        return Command.fail(reason="bad pkg")
    if(not form.has_key("CMD")):
        return Command.fail(reason="bad cmd")
    args = {}
    for k in form.keys():
        if(not isinstance(k, str)):continue
        if(k==""):continue
        if(k[:1]=="_"):continue
        if(k=="CMD"):continue
        if(k=="PKG"):continue
        if(k.startswith("file_")):
            v = form[k].file
            if not v:continue
            args[k] = v
        else:
            v = form[k].value
            if(not isinstance(v, str)):continue
            args[k] = v
    args["env_ip"] = cgi.escape(os.environ["REMOTE_ADDR"])
    return Command.call(form["PKG"].value, form["CMD"].value, args)

ret = action()

print json.dumps(ret)
