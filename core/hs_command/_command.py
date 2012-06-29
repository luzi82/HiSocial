import hs_command

def command_guest_list_cmd():
    '''
    List all command
    wrapper of base.hs_command.list_cmd()
    
    @rtype: dict
    @return: ["value"] = base.hs_command.list_cmd() output
    '''
    return hs_command.ok({"value":hs_command.list_cmd()})
