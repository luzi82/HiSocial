#!/usr/bin/python

import sys
import cgi_config
sys.path.insert(0, cgi_config.CORE_PATH)

import cgi
from base import Command
import json

print "Content-Type: text/plain; charset=utf-8"
print

form = cgi.FieldStorage()

def action():
    if(not form.has_key("pkg")):
        return Command.fail(reason="bad pkg")
    if(not form.has_key("cmd")):
        return Command.fail(reason="bad cmd")
    args = {}
    for k in form.keys():
        v = form[k].value
        if(not isinstance(k, str)):
            continue
        if(not isinstance(v, str)):
            continue
        if(not k.startswith("_")):
            continue
        args[k[1:]] = form[k].value
    return Command.call(form["pkg"].value, form["cmd"].value, args)

ret = action()

print json.dumps(ret)
