from BitTorrent import bencode
from HiFile import Torrent
import hashlib
import pprint
import unittest

class TestTorrent(unittest.TestCase):
    
    pp = pprint.PrettyPrinter()
    
    def test_parse(self):
        data=Torrent.parse_torrent("res/test0.torrent")
#        pp.pprint(data)
        info=data["info"]
        info_hash_hex = hashlib.sha1(bencode.bencode(info)).hexdigest()
        self.assertEqual(info_hash_hex, "2034385a2621c53a490f34c5893a860664741da4")
        self.assertEqual(Torrent.get_info_hash_hex(data), "2034385a2621c53a490f34c5893a860664741da4")
