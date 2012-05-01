import turing
from base import Command

def COMMAND_guest_test_turing(turing_value,_ip):
    '''
    Check recaptcha, wrapper of turing.check_recaptcha.
    
    @type  turing_value: str
    @param turing_value: turing value in JSON format, should have turing_value["challenge"] and turing_value["response"]
    @type  _ip: str
    @param _ip: IP of client
    
    @rtype: dict
    @return: Command response, OK iff success
    '''
    if not turing.check_recaptcha(turing_value,_ip):
        return Command.fail()
    return Command.ok()
