from base import Command
from recaptcha.client import captcha
import core_config
import json

def public_guest_test_turing(turing_input,_ip):
    if not isinstance(turing_input, str):
        return Command.fail()
    if not isinstance(_ip, str):
        return Command.fail()
    v = json.loads(s=turing_input,encoding="utf8")
    if not isinstance(v, dict):
        return Command.fail()
    if not isinstance(v["challenge"], unicode):
        return Command.fail()
    if not isinstance(v["response"], unicode):
        return Command.fail()
    output = captcha.submit(v["challenge"], v["response"], core_config.RECAPTCHA_PRIVATE_KEY, _ip)
    if not output.is_valid:
        return Command.fail(reason="not valid")
    return Command.ok()
