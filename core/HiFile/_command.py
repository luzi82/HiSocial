import HiFile.Torrent
from base import Command, Database
from base.Cleanup import Cleanup
import _database
import pprint
import user.UserLoginToken
import TrackerManager
from HiFile import TorrentStorage
import time
import HiFile

def command_user_upload_torrent(txtf_user_token_user, file_torrent):
#    actor_id = user.UserLoginToken.check_user_login_token(user_login_token)
#    if actor_id == None:
#        return Command.fail(reason="user_login_token")
    
    file_bin = file_torrent.read()
    
    torrent_data = HiFile.Torrent.parse_torrent_data(file_bin)
    info_hash_hex = HiFile.Torrent.get_info_hash_hex(torrent_data)
    name = HiFile.Torrent.get_name(torrent_data)
    size = HiFile.Torrent.get_total_size(torrent_data)
    
    cleanup = Cleanup()
    session = Database.create_sqlalchemy_session_push(cleanup)
    
    torrent_id = _database.add_torrent(session, txtf_user_token_user, info_hash_hex, name, size)
    TrackerManager.add_hash(session, info_hash_hex)
    
    session.commit()
    cleanup.clean_all()
    
    TorrentStorage.store_torrent(torrent_id, file_bin)
    
    return Command.ok(result={"torrent_id":torrent_id})

def command_user_list_user_torrent(txtf_user_token_user, txt_user_id):
#    actor_id = user.UserLoginToken.check_user_login_token(user_login_token)
#    if actor_id == None:
#        return Command.fail(reason="user_login_token")
    
    if txt_user_id != txtf_user_token_user:
        return Command.fail(reason="no permission")
    
    cleanup = Cleanup()
    session = Database.create_sqlalchemy_session_push(cleanup)

    torrent_list = _database.list_user_torrent(session, txt_user_id)

    session.commit()
    cleanup.clean_all()
    
    now = int(time.time())
    
    ret = [ dict((k, d[k])for k in ["torrent_id", "name", "size"]) for d in torrent_list ]
    for r in ret:
        r["torrent_token"]=HiFile.generate_torrent_token(r["torrent_id"],now,now+600,txt_user_id)
    
    return Command.ok(result={"torrent_list":ret})

def command_guest_get_torrent_data(txtf_HiFile_torrenttoken_torrent):
#    ret = HiFile.verify_torrent_token(txt_torrent_token)
#    if(ret == None):
#        return Command.fail(reason="torrent_token",result={"torrent_token":txt_torrent_token})
    
    cleanup = Cleanup()
    session = Database.create_sqlalchemy_session_push(cleanup)
    
    torrent_data = _database.get_torrent_data(session, txtf_HiFile_torrenttoken_torrent)

    return Command.ok(result={"torrent_data":torrent_data})

def argfilter_torrenttoken(v):
    ret = HiFile.verify_torrent_token(v)
    if(ret == None):
        return Command.fail(reason="bad torrent token")
    return Command.ok(value=ret)

#def command_test(FILE_in):
#    file_bin=FILE_in.read()
#    torrent_data = HiFile.Torrent.parse_torrent_data(file_bin)
#    return Command.ok(result={"info_hash_hex":HiFile.Torrent.get_info_hash_hex(torrent_data)})
