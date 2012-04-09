from base import Secret
import core_config
import time

def generate_torrent_token(torrent_id, time_start, time_end, token_creator_user_id):
    data = { \
        "torrent_id":torrent_id, \
        "time_start":time_start, \
        "time_end":time_end, \
        "token_creator_user_id":token_creator_user_id, \
    }
    return Secret.encrypt(data, core_config.HIFILE_HASH_HMAC, core_config.HIFILE_HASH_HMAC)

def verify_torrent_token(token):
    data = Secret.decrypt(token, core_config.HIFILE_HASH_HMAC, core_config.HIFILE_HASH_HMAC)
    if(data == None):return None
    now = int(time.time())
    if(data["time_start"] > now):return None
    if(data["time_end"] < now):return None
    # need to do sth for token_creator_user_id
    return data["torrent_id"]
