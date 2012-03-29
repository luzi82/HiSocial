import HiFile.Torrent
from base import Command, Database
from base.Cleanup import Cleanup
import _database
import pprint
import user.UserLoginToken
import TrackerManager
from HiFile import TorrentStorage

def public_user_upload_torrent(user_login_token,FILE_torrent):
    actor_id = user.UserLoginToken.check_user_login_token(user_login_token)
    if actor_id == None:
        return Command.fail(reason="user_login_token")
    
    file_bin=FILE_torrent.read()
    torrent_data = HiFile.Torrent.parse_torrent_data(file_bin)
    info_hash_hex = HiFile.Torrent.get_info_hash_hex(torrent_data)
    name = HiFile.Torrent.get_name(torrent_data)
    size = HiFile.Torrent.get_total_size(torrent_data)
    
    cleanup = Cleanup()
    session = Database.create_sqlalchemy_session_push(cleanup)
    
    torrent_id=_database.add_torrent(session, actor_id,info_hash_hex,name,size)
    TrackerManager.add_hash(session, info_hash_hex)
    
    session.commit()
    cleanup.clean_all()
    
    TorrentStorage.store_torrent(torrent_id,file_bin)
    
    return Command.ok(result={"torrent_id":torrent_id})

def public_user_list_user_torrent(user_login_token,user_id):
    actor_id = user.UserLoginToken.check_user_login_token(user_login_token)
    if actor_id == None:
        return Command.fail(reason="user_login_token")
    
    if user_id != actor_id:
        return Command.fail(reason="no permission")
    
    cleanup = Cleanup()
    session = Database.create_sqlalchemy_session_push(cleanup)

    torrent_list=_database.list_user_torrent(session,user_id)

    session.commit()
    cleanup.clean_all()
    
    return Command.ok(result={"torrent_list":torrent_list})

def public_test(FILE_in):
    file_bin=FILE_in.read()
    torrent_data = HiFile.Torrent.parse_torrent_data(file_bin)
    return Command.ok(result={"info_hash_hex":HiFile.Torrent.get_info_hash_hex(torrent_data)})
