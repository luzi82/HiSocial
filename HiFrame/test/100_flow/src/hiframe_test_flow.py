import unittest
from hiframe import hiframe
import os
import shutil

MY_ABSOLUTE_PATH = os.path.abspath(__file__)
MY_ABSOLUTE_PARENT = os.path.dirname(MY_ABSOLUTE_PATH)
MY_ABSOLUTE_PARENT2 = os.path.dirname(MY_ABSOLUTE_PARENT)
DATA_PATH = MY_ABSOLUTE_PARENT2+"/tmp"

class HiframeTestFlow(unittest.TestCase):
    
    def setUp(self):
        shutil.rmtree(DATA_PATH)

    def test_flow_0(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],data_path=DATA_PATH)
        hf.build()
        hf.start()
        hf.end()
        hf.clean()

    def test_flow_1(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],data_path=DATA_PATH)
        hf.build()
        hf.clean()

    def test_build_twice(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],data_path=DATA_PATH)
        hf.build()
        hf.build()

    def test_clean_twice(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],data_path=DATA_PATH)
        hf.build()
        hf.clean()
        hf.clean()
