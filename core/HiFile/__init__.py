from hs_common import hs_secret
import core_config
import time

STORAGE_PATH = core_config.DATA_FOLDER+"/HiFile"

def generate_torrent_token(torrent_id, time_start, time_end, token_creator_user_id):
    data = { \
        "torrent_id":torrent_id, \
        "time_start":time_start, \
        "time_end":time_end, \
        "token_creator_user_id":token_creator_user_id, \
    }
    return hs_secret.encrypt(data, core_config.HIFILE_ENC_KEY)

def verify_torrent_token(token):
    data = hs_secret.decrypt(token, core_config.HIFILE_ENC_KEY)
    if(data == None):return None
    now = int(time.time())
    if(data["time_start"] > now):return None
    if(data["time_end"] < now):return None
    # need to do sth for token_creator_user_id
    return data["torrent_id"]
