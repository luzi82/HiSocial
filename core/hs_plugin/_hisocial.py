import hs_plugin

def command_guest_list_cmd():
    '''
    List all command
    wrapper of base.hs_plugin.list_cmd()
    
    @rtype: dict
    @return: ["value"] = base.hs_plugin.list_cmd() output
    '''
    return hs_plugin.ok({"value":hs_plugin.list_cmd()})
