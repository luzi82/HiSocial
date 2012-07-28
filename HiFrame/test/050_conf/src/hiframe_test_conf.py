import unittest
import hiframe
import os

MY_ABSOLUTE_PATH = os.path.abspath(__file__)
MY_ABSOLUTE_PARENT = os.path.dirname(MY_ABSOLUTE_PATH)
TEST_FOLDER = os.path.dirname(MY_ABSOLUTE_PARENT)
RES_FOLDER = TEST_FOLDER+"/res"

class HiframeTestConf(unittest.TestCase):

    def test_basic(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],filename="_hiframe",conf_file=RES_FOLDER+"/basic.conf")
        config = hf.get_config()
        self.assertIsNotNone(config)
        self.assertEqual(config.get("test1","abc"), "def")
        
    def test_conf_not_exist(self):
        try:
            hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],filename="_hiframe",conf_file=RES_FOLDER+"/not_exist.conf")
            # bad
            self.fail()
        except IOError:
            # good
            pass

    def test_conf_none(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT])
        config = hf.get_config()
        self.assertIsNone(config)
