import turing
from base import Command

def command_guest_test_turing(txtf_turing_turing,env_ip):
    '''
    Check recaptcha, wrapper of turing.check_recaptcha.
    
    @type  turing_value: str
    @param turing_value: turing value in JSON format, should have turing_value["challenge"] and turing_value["response"]
    @type  env_ip: str
    @param env_ip: IP of client
    
    @rtype: dict
    @return: Command response, OK iff success
    '''
    return Command.ok()

def argfilter_turing(v,env_ip):
    if not turing.check_recaptcha(v,env_ip):
        return Command.fail(reason="bad turing value")
    return Command.ok(value="")
