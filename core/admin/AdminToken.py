from base import Secret
import core_config
import time

def generate_admin_token(deadline=None):
    if(deadline == None):
        now = int(time.time())
        deadline = now + core_config.ADMIN_TOKEN_VALID_TIME_PERIOD
    return Secret.encrypt(deadline, core_config.ADMIN_TOKEN_HASH_HMAC, core_config.ADMIN_TOKEN_ENC_KEY)

def check_admin_token(admin_token):
    if(admin_token == None):
        return False
    if(not isinstance(admin_token, str)):
        return False
    v = Secret.decrypt(admin_token, core_config.ADMIN_TOKEN_HASH_HMAC, core_config.ADMIN_TOKEN_ENC_KEY)
    if(v == None):
        return False
    now = int(time.time())
    return now < v
