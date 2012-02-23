from base import Command
import string
import Version

def public_guest_get_version():
    return Command.ok({"version":Version.VERSION, "type":Version.TYPE})

def public_guest_ping(value):
    '''
    Ping the system
    
    :param value: len-8 hex string
    
    :return: value=~(value), len-8 hex string.  No value if bad input.
    '''
    BAD_VALUE = Command.fail(reason="bad value")
    if(len(value) != 8):return BAD_VALUE
    for c in value : 
        if c not in string.hexdigits: return BAD_VALUE
    t = int(value, 16)
    t = ~t
    t = ("00000000%x" % (t & 0xffffffff))[-8:]
    return Command.ok({"value":t})

def public_guest_list_cmd():
    return Command.ok({"value":Command.list_cmd()})
