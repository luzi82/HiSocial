import core_config

STORAGE_PATH = core_config.DATA_FOLDER+"/HiFile/torrent"

def store_torrent(torrent_id,file_bin):
    file_path=_torrentid_to_path(torrent_id)
    f = open(file_path,"wb")
    f.write(file_bin)
    f.flush()
    f.close()

def _torrentid_to_path(torrent_id):
    return STORAGE_PATH+("/%08x"%(torrent_id))
