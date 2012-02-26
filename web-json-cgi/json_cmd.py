#!/usr/bin/python

import sys
import webjsoncgi_config
sys.path.insert(0, webjsoncgi_config.CORE_PATH)

import cgi
from base import Command
import json

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
        v = form[k].value
        if(not isinstance(k, str)):continue
        if(k=="CMD"):continue
        if(k=="PKG"):continue
        if(not isinstance(v, str)):continue
        args[k] = form[k].value
    return Command.call(form["PKG"].value, form["CMD"].value, args)

ret = action()

print json.dumps(ret)
