from admin import AdminToken
from base import Command
import core_config

def guest_generate_admin_token(password):
    '''
    Generate admin token
    '''
    if(password != core_config.ADMIN_PASSWORD):
        return Command.fail(reason="auth fail")
    token = AdminToken.generate_admin_token()
    return Command.ok({"admin_token":token})
