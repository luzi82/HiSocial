from hicommon import crypto
import core_config
import time

def generate_user_login_token(user_id,deadline=None):
    if(deadline == None):
        now = int(time.time())
        deadline = now + core_config.USER_TOKEN_VALID_TIME_PERIOD
    return crypto.encrypt({"user_id":user_id,"deadline":deadline}, core_config.USER_TOKEN_ENC_KEY)

def check_user_login_token(user_login_token):
    if(user_login_token == None):
        return None
    if(not isinstance(user_login_token, str)):
        return None
    v = crypto.decrypt(user_login_token, core_config.USER_TOKEN_ENC_KEY)
    if(v == None):
        return None
    now = int(time.time())
    if now > v["deadline"]:
        return None
    return v["user_id"]
