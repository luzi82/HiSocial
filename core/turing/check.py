from recaptcha.client import captcha
import core_config
import json

def check_recaptcha(turing_input,_ip):
    if not isinstance(turing_input, str):
        return False
    if not isinstance(_ip, str):
        return False
    v = json.loads(s=turing_input,encoding="utf8")
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
