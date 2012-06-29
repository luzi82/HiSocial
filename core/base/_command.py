from hs_command import hs_command
import string
import Version

def command_guest_get_version():
    """
    Return the HiSocial version info
    
    @rtype: dict
    @return: ret["version"] current version. ret["type"] "development" or "production"
    """
    return hs_command.ok({"version":Version.VERSION, "type":Version.TYPE})

def command_guest_ping(txt_value):
    '''
    Ping the system
    
    @type txt_value: str
    @param txt_value: len-8 hex string
    
    @rtype: dict
    @return: ret["value"]=~(txt_value), len-8 hex string.  No value if bad input.
    '''
    BAD_VALUE = hs_command.fail(reason="bad value")
    if(len(txt_value) != 8):return BAD_VALUE
    for c in txt_value : 
        if c not in string.hexdigits: return BAD_VALUE
    t = int(txt_value, 16)
    t = ~t
    t = ("00000000%x" % (t & 0xffffffff))[-8:]
    return hs_command.ok({"value":t})

def command_guest_list_cmd():
    '''
    List all command
    wrapper of base.hs_command.list_cmd()
    
    @rtype: dict
    @return: ["value"] = base.hs_command.list_cmd() output
    '''
    return hs_command.ok({"value":hs_command.list_cmd()})
