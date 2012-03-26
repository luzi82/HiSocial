from BitTorrent import bencode
import hashlib

def parse_torrent(torrent):
    if (isinstance(torrent, str)):
        return bencode.bdecode(open(torrent,"rb").read())
    elif (isinstance(torrent, file)):
        return bencode.bdecode(torrent.read())
    return None

def get_info_hash_hex(torrent_data):
    return hashlib.sha1(bencode.bencode(torrent_data["info"])).hexdigest()
