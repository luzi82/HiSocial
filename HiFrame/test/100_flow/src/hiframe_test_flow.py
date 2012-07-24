import unittest
from hiframe import hiframe
import os
import shutil
import hiframe_test_flow_plugin._hiframe as test_hiframe

MY_ABSOLUTE_PATH = os.path.abspath(__file__)
MY_ABSOLUTE_PARENT = os.path.dirname(MY_ABSOLUTE_PATH)
MY_ABSOLUTE_PARENT2 = os.path.dirname(MY_ABSOLUTE_PARENT)
WORKING_PATH = MY_ABSOLUTE_PARENT2
DATA_PATH = WORKING_PATH+"/tmp"
CONF_FILE = WORKING_PATH+"/res/setting.conf"
CONF_FILE_NODATAPATH = WORKING_PATH+"/res/no_data_path.conf"

class HiframeTestFlow(unittest.TestCase):
    
    def setUp(self):
        os.chdir(WORKING_PATH)
        if os.path.exists(DATA_PATH):
            shutil.rmtree(DATA_PATH)
        test_hiframe.BUILD_COUNT=0
        test_hiframe.CLEAN_COUNT=0
        test_hiframe.START_COUNT=0
        test_hiframe.STOP_COUNT=0

    def tearDown(self):
        if os.path.exists(DATA_PATH):
            shutil.rmtree(DATA_PATH)

    def test_flow_0(self):
        self.assertFalse(os.path.exists(DATA_PATH))
        
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],conf_file=CONF_FILE)
        self.assertFalse(os.path.exists(DATA_PATH))
        
        hf.build()
        self.assertEqual(test_hiframe.BUILD_COUNT,1)
        self.assertTrue(os.path.exists(DATA_PATH))
        
        hf.start()
        self.assertEqual(test_hiframe.START_COUNT,1)
        self.assertTrue(os.path.exists(DATA_PATH))
        
        hf.stop()
        self.assertEqual(test_hiframe.STOP_COUNT,1)
        self.assertTrue(os.path.exists(DATA_PATH))
        
        hf.clean()
        self.assertEqual(test_hiframe.CLEAN_COUNT,1)
        self.assertFalse(os.path.exists(DATA_PATH))

    def test_flow_1(self):
        self.assertFalse(os.path.exists(DATA_PATH))
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],conf_file=CONF_FILE)
        self.assertFalse(os.path.exists(DATA_PATH))
        hf.build()
        self.assertEqual(test_hiframe.BUILD_COUNT,1)
        self.assertTrue(os.path.exists(DATA_PATH))
        hf.clean()
        self.assertEqual(test_hiframe.CLEAN_COUNT,1)
        self.assertFalse(os.path.exists(DATA_PATH))

    def test_build_twice(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],conf_file=CONF_FILE)
        hf.build()
        self.assertEqual(test_hiframe.BUILD_COUNT,1)
        hf.build()
        self.assertEqual(test_hiframe.BUILD_COUNT,1)

    def test_clean_twice(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],conf_file=CONF_FILE)
        hf.build()
        self.assertEqual(test_hiframe.BUILD_COUNT,1)
        hf.clean()
        self.assertEqual(test_hiframe.CLEAN_COUNT,1)
        hf.clean()
        self.assertEqual(test_hiframe.CLEAN_COUNT,1)

    def test_start_twice(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],conf_file=CONF_FILE)
        hf.start()
        self.assertEqual(test_hiframe.START_COUNT,1)
        hf.start()
        self.assertEqual(test_hiframe.START_COUNT,1)

    def test_stop_twice(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],conf_file=CONF_FILE)
        hf.start()
        hf.stop()
        self.assertEqual(test_hiframe.STOP_COUNT,1)
        hf.stop()
        self.assertEqual(test_hiframe.STOP_COUNT,1)

    def test_auto_build(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],conf_file=CONF_FILE)
        hf.start()
        self.assertEqual(test_hiframe.BUILD_COUNT,1)
        self.assertEqual(test_hiframe.START_COUNT,1)

    def test_auto_stop(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],conf_file=CONF_FILE)
        hf.start()
        hf.clean()
        self.assertEqual(test_hiframe.STOP_COUNT,1)
        self.assertEqual(test_hiframe.CLEAN_COUNT,1)

    def test_build_clean_build_clean(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],conf_file=CONF_FILE)

        hf.build()
        self.assertEqual(test_hiframe.BUILD_COUNT,1)
        self.assertTrue(os.path.exists(DATA_PATH))
        
        hf.clean()
        self.assertEqual(test_hiframe.CLEAN_COUNT,1)
        self.assertFalse(os.path.exists(DATA_PATH))

        hf.build()
        self.assertEqual(test_hiframe.BUILD_COUNT,2)
        self.assertTrue(os.path.exists(DATA_PATH))
        
        hf.clean()
        self.assertEqual(test_hiframe.CLEAN_COUNT,2)
        self.assertFalse(os.path.exists(DATA_PATH))

    def test_start_stop_start_stop(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],conf_file=CONF_FILE)

        hf.start()
        self.assertEqual(test_hiframe.START_COUNT,1)
        
        hf.stop()
        self.assertEqual(test_hiframe.STOP_COUNT,1)

        hf.start()
        self.assertEqual(test_hiframe.START_COUNT,2)
        
        hf.stop()
        self.assertEqual(test_hiframe.STOP_COUNT,2)

    def test_no_data(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],conf_file=CONF_FILE_NODATAPATH)

        hf.start()
        self.assertEqual(test_hiframe.START_COUNT,1)
        
        hf.stop()
        self.assertEqual(test_hiframe.STOP_COUNT,1)
