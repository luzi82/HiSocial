from BitTorrent import bencode
import hashlib

def parse_torrent(torrent):
    if (isinstance(torrent, str)):
        return parse_torrent_data(open(torrent,"rb").read())
    elif (isinstance(torrent, file)):
        return parse_torrent_data(torrent.read())
    return None

def parse_torrent_data(data):
    return bencode.bdecode(data)

def get_info_hash_hex(torrent_data):
    return hashlib.sha1(bencode.bencode(torrent_data["info"])).hexdigest()

def get_name(torrent_data):
    info=torrent_data["info"]
    if("name.utf-8" in info):
        return info["name.utf-8"]
    else:
        return info["name"]

def get_total_size(torrent_data):
    ret=0
    info_files=torrent_data["info"]["files"]
    for i in info_files:
        ret+=i["length"]
    return ret