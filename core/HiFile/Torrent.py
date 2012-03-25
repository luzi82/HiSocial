from BitTorrent import bencode
import hashlib

def parse_torrent(torrent_filename):
    return bencode.bdecode(open(torrent_filename,"rb").read())

def get_info_hash_hex(torrent_data):
    return hashlib.sha1(bencode.bencode(torrent_data["info"])).hexdigest()
