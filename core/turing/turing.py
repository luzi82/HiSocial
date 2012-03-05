from recaptcha.client import captcha
import core_config
import json

force_output = None

def check_recaptcha(turing_value,_ip):
    '''
    Check recaptcha

    @type turing_value: str
    @param turing_value: turing value in JSON format, should have turing_value["challenge"] and turing_value["response"]
    @type _ip: str
    @param _ip: IP of client

    @rtype: boolean
    @return: True iff recaptcha pass
    '''
    if force_output != None:
        return force_output
    if not isinstance(turing_value, str):
        return False
    if not isinstance(_ip, str):
        return False
    v = json.loads(s=turing_value,encoding="utf8")
    if not isinstance(v, dict):
        return False
    if not isinstance(v["challenge"], unicode):
        return False
    if not isinstance(v["response"], unicode):
        return False
    output = captcha.submit(v["challenge"], v["response"], core_config.RECAPTCHA_PRIVATE_KEY, _ip)
    if not output.is_valid:
        return False
    return True
