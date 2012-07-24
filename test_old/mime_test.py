import unittest
from hs_common import hs_mime

class mime_test(unittest.TestCase):
    
    def test_torrent(self):
        ret = hs_mime.read_file("res/test0.torrent")
        self.assertEqual(ret,"application/x-bittorrent; charset=binary")

    def test_image(self):
        ret = hs_mime.read_file("res/math0.png")
        self.assertEqual(ret,"image/png; charset=binary")

    def test_html(self):
        ret = hs_mime.read_file("res/html_simple_0.html")
        self.assertEqual(ret,"application/xml; charset=utf-8")

        ret = hs_mime.read_file("res/html_simple_1.html")
        self.assertEqual(ret,"text/html; charset=utf-8")

        ret = hs_mime.read_file("res/html_simple_2.html")
        self.assertEqual(ret,"application/xml; charset=utf-8")

        ret = hs_mime.read_file("res/html_simple_3.xml")
        self.assertEqual(ret,"application/xml; charset=utf-8")
