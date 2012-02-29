from turing import check
from base import Command

def public_guest_test_turing(turing_input,_ip):
    if not check.check_recaptcha(turing_input,_ip):
        return Command.fail()
    return Command.ok()
