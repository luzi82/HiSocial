from base import Command
from recaptcha.client import captcha
import core_config
import json

def public_guest_test_turing(turing_input,_ip):
    a=""
    try:
        v = json.loads(turing_input)
        output = captcha.submit(v["challenge"], v["response"], core_config.RECAPTCHA_PRIVATE_KEY, _ip)
        if not output.is_valid:
            return Command.fail(turing_input)
        return Command.ok()
    except Exception:
        return Command.fail()
