# -*- coding: utf-8 -*-

from BitTorrent import bencode
from HiFile import Torrent
import hashlib
import pprint
import unittest

class TestTorrent(unittest.TestCase):
    
    pp = pprint.PrettyPrinter()
    
    def test_parse(self):
        data=Torrent.parse_torrent("res/test0.torrent")
        info=data["info"]
        info_hash_hex = hashlib.sha1(bencode.bencode(info)).hexdigest()
        self.assertEqual(info_hash_hex, "2034385a2621c53a490f34c5893a860664741da4")
        self.assertEqual(Torrent.get_info_hash_hex(data), "2034385a2621c53a490f34c5893a860664741da4")
        self.assertEqual(Torrent.get_name(data),"Super Eurobeat Vol. 220 - Anniversary Hits")
        
        data=Torrent.parse_torrent(open("res/test0.torrent","rb"))
        info=data["info"]
        info_hash_hex = hashlib.sha1(bencode.bencode(info)).hexdigest()
        self.assertEqual(info_hash_hex, "2034385a2621c53a490f34c5893a860664741da4")
        self.assertEqual(Torrent.get_info_hash_hex(data), "2034385a2621c53a490f34c5893a860664741da4")
        self.assertEqual(Torrent.get_name(data),"Super Eurobeat Vol. 220 - Anniversary Hits")

        data=Torrent.parse_torrent_data(open("res/test0.torrent","rb").read())
        info=data["info"]
        info_hash_hex = hashlib.sha1(bencode.bencode(info)).hexdigest()
        self.assertEqual(info_hash_hex, "2034385a2621c53a490f34c5893a860664741da4")
        self.assertEqual(Torrent.get_info_hash_hex(data), "2034385a2621c53a490f34c5893a860664741da4")
        self.assertEqual(Torrent.get_name(data),"Super Eurobeat Vol. 220 - Anniversary Hits")

    def test_unicode(self):
        data=Torrent.parse_torrent("res/test1.torrent")
        self.assertEqual(len(data["info"]["files"][1]["path"]),1)
        self.assertEqual(data["info"]["files"][1]["path"][0], "[EAC](アルバム)「ARIA The ANIMATION」 オリジナルサウンドトラック (ape+cue+rr3).rar")
        
        data=Torrent.parse_torrent("res/test2.torrent")
        self.assertEqual(data["info"]["name"],"魔法少女小圓")
        self.assertEqual(Torrent.get_name(data),"魔法少女小圓")
        

#    def test_show(self):
#        data=Torrent.parse_torrent("res/test2.torrent")
#        self.pp.pprint(data)
        