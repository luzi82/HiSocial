import unittest
from hicommon import mime
import os

MY_ABSOLUTE_PATH = os.path.abspath(__file__)
MY_ABSOLUTE_PARENT = os.path.dirname(MY_ABSOLUTE_PATH)
MY_ABSOLUTE_PARENT2 = os.path.dirname(MY_ABSOLUTE_PARENT)
WORKING_PATH = MY_ABSOLUTE_PARENT2

class mime_test(unittest.TestCase):
    
    def setUp(self):
        os.chdir(WORKING_PATH)
    
    def test_torrent(self):
        ret = mime.read_file("res/test0.torrent")
        self.assertEqual(ret,"application/x-bittorrent; charset=binary")

    def test_image(self):
        ret = mime.read_file("res/math0.png")
        self.assertEqual(ret,"image/png; charset=binary")

    def test_html(self):
        ret = mime.read_file("res/html_simple_0.html")
        self.assertEqual(ret,"application/xml; charset=utf-8")

        ret = mime.read_file("res/html_simple_1.html")
        self.assertEqual(ret,"text/html; charset=utf-8")

        ret = mime.read_file("res/html_simple_2.html")
        self.assertEqual(ret,"application/xml; charset=utf-8")

        ret = mime.read_file("res/html_simple_3.xml")
        self.assertEqual(ret,"application/xml; charset=utf-8")
