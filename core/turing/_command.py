import turing
from base import Command

def public_guest_test_turing(turing_value,_ip):
    if not turing.check_recaptcha(turing_value,_ip):
        return Command.fail()
    return Command.ok()
