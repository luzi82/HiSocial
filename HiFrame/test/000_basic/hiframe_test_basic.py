import unittest
from hiframe import hiframe
import os
import hiframe_test_basic_plugin._hiframe

MY_ABSOLUTE_PATH = os.path.abspath(__file__)
MY_ABSOLUTE_PARENT = os.path.dirname(MY_ABSOLUTE_PATH)

class HiframeTestBasic(unittest.TestCase):

    def test_scan(self):
        tmp = hiframe._scan_func(plugin_path_list=[MY_ABSOLUTE_PARENT],filename="_hiframe")
        self.assertEqual(tmp["simple"][0][0]["call"], hiframe_test_basic_plugin._hiframe.simple_func)
        self.assertEqual(tmp["simple"][0][0]["pkg"], "hiframe_test_basic_plugin")
        self.assertEqual(tmp["simple"][0][0]["func"], "simple_func")
        
    def test_call(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],filename="_hiframe")
        tmp = hf.call("simple")
        self.assertEqual(tmp,[{
            "pkg":"hiframe_test_basic_plugin",
            "func":"simple_func",
            "ret":"simple ret"
        }])
        tmp = hf.call("simple_arg",args={"abc":100})
        self.assertEqual(tmp,[{
            "pkg":"hiframe_test_basic_plugin",
            "func":"simple_arg_func",
            "ret":101
        }])

    def test_order(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],filename="_hiframe")

        self.assertEqual(hf._func_dict["order"][-1][0]["call"], hiframe_test_basic_plugin._hiframe.order_c)
        self.assertEqual(hf._func_dict["order"][0][0]["call"], hiframe_test_basic_plugin._hiframe.order_a)
        self.assertEqual(hf._func_dict["order"][1][0]["call"], hiframe_test_basic_plugin._hiframe.order_b)

        tmp = hf.call("order")
        self.assertEqual(tmp,[
            {
                "pkg":"hiframe_test_basic_plugin",
                "func":"order_c",
                "ret":"c"
            },
            {
                "pkg":"hiframe_test_basic_plugin",
                "func":"order_a",
                "ret":"a"
            },
            {
                "pkg":"hiframe_test_basic_plugin",
                "func":"order_b",
                "ret":"b"
            },
        ])

    def test_pkg2(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],filename="_hiframe")
        tmp = hf.call("pkg2")
        self.assertEqual(tmp,[
            {
                "pkg":"hiframe_test_basic_plugin",
                "func":"pkg2_c",
                "ret":"c"
            },
            {
                "pkg":"hiframe_test_basic_plugin2",
                "func":"pkg2_b",
                "ret":"b"
            },
            {
                "pkg":"hiframe_test_basic_plugin",
                "func":"pkg2_a",
                "ret":"a"
            },
        ])
        
    def test_no_order(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],filename="_hiframe")
        tmp = hf.call("no_order")
        self.assertTrue({
            "pkg":"hiframe_test_basic_plugin",
            "func":"no_order_a",
            "ret":"a"
        } in tmp)
        self.assertTrue({
            "pkg":"hiframe_test_basic_plugin",
            "func":"no_order_b",
            "ret":"b"
        } in tmp)
        self.assertEqual(len(tmp),2)

    def test_abc(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],filename="_abc")
        tmp = hf.call("abc key")
        self.assertEqual(tmp,[{
            "pkg":"hiframe_test_basic_plugin",
            "func":"abc_func",
            "ret":"abc ret"
        }])
