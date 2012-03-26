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
