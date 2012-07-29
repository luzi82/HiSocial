import HiFile.Torrent
from base import Database
from hicommon.cleanup import Cleanup
import _database
import TrackerManager
from HiFile import TorrentStorage
import time
from hs_plugin import hs_plugin

def command_user_upload_torrent(txtf_user_token_user, file_torrent):
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
    
    return hs_plugin.ok(result={"torrent_id":torrent_id})

def command_user_list_user_torrent(txtf_user_token_user, txt_user_id):
    if txt_user_id != txtf_user_token_user:
        return hs_plugin.fail(reason="no permission")
    
    cleanup = Cleanup()
    session = Database.create_sqlalchemy_session_push(cleanup)

    torrent_list = _database.list_user_torrent(session, txt_user_id)

    session.commit()
    cleanup.clean_all()
    
    now = int(time.time())
    
    ret = [ dict((k, d[k])for k in ["torrent_id", "name", "size"]) for d in torrent_list ]
    for r in ret:
        r["torrent_token"]=HiFile.generate_torrent_token(r["torrent_id"],now,now+600,txt_user_id)
    
    return hs_plugin.ok(result={"torrent_list":ret})

def command_guest_get_torrent_data(txtf_HiFile_torrenttoken_torrent):
    cleanup = Cleanup()
    session = Database.create_sqlalchemy_session_push(cleanup)
    
    torrent_data = _database.get_torrent_data(session, txtf_HiFile_torrenttoken_torrent)

    return hs_plugin.ok(value=torrent_data)

def file_guest_get_torrent(txtf_HiFile_torrenttoken_torrent):
    torrent_path=TorrentStorage._torrentid_to_path(txtf_HiFile_torrenttoken_torrent)

    cleanup = Cleanup()
    session = Database.create_sqlalchemy_session_push(cleanup)
    torrent_data = _database.get_torrent_data(session, txtf_HiFile_torrenttoken_torrent)
    cleanup.clean_all()
    
    return hs_plugin.ok(result={
        "file_type":"local",
        "file_name":torrent_path,
        "output_name":torrent_data["name"]+".torrent",
    })

def argfilter_torrenttoken(v):
    ret = HiFile.verify_torrent_token(v)
    if(ret == None):
        return hs_plugin.fail(reason="bad torrent token")
    return hs_plugin.ok(value=ret)
