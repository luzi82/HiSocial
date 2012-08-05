import unittest
import hiframe
import os
import hiframe_test_basic_plugin._hiframe

MY_ABSOLUTE_PATH = os.path.abspath(__file__)
MY_ABSOLUTE_PARENT = os.path.dirname(MY_ABSOLUTE_PATH)

class HiframeTestBasic(unittest.TestCase):

    def test_scan_plugin(self):
        tmp = hiframe._scan_plugin(plugin_path_list=[MY_ABSOLUTE_PARENT],filename_list=["_hiframe"],hf=None)
        self.assertTrue("hiframe_test_basic_plugin" in tmp)
        self.assertTrue("hiframe_test_basic_plugin2" in tmp)
        self.assertEqual(tmp["hiframe_test_basic_plugin"]["module"], "_hiframe")
        self.assertEqual(tmp["hiframe_test_basic_plugin"]["class"], "HiframeTestBasicPlugin")
        self.assertTrue(isinstance(tmp["hiframe_test_basic_plugin"]["obj"], hiframe_test_basic_plugin._hiframe.HiframeTestBasicPlugin))
        
    def test_scan_func(self):
        plugin_list = hiframe._scan_plugin(plugin_path_list=[MY_ABSOLUTE_PARENT],filename_list=["_hiframe"],hf=None)

        tmp = hiframe._scan_func(plugin_list=plugin_list)
        self.assertEqual(tmp["simple"][0]["call"], hiframe_test_basic_plugin._hiframe.HiframeTestBasicPlugin.simple_func)
        self.assertEqual(tmp["simple"][0]["pkg"], "hiframe_test_basic_plugin")
        self.assertEqual(tmp["simple"][0]["module"], "_hiframe")
        self.assertEqual(tmp["simple"][0]["class"], "HiframeTestBasicPlugin")
        self.assertTrue(isinstance(tmp["simple"][0]["obj"], hiframe_test_basic_plugin._hiframe.HiframeTestBasicPlugin))
        self.assertEqual(tmp["simple"][0]["func"], "simple_func")
        
    def test_call(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT])
        tmp = hf.call("simple")
        self.assertEqual(tmp,[{
            "pkg":"hiframe_test_basic_plugin",
            "module":"_hiframe",
            "class":"HiframeTestBasicPlugin",
            "func":"simple_func",
            "ret":"simple ret"
        }])
        tmp = hf.call("simple_arg",args={"abc":100})
        self.assertEqual(tmp,[{
            "pkg":"hiframe_test_basic_plugin",
            "module":"_hiframe",
            "class":"HiframeTestBasicPlugin",
            "func":"simple_arg_func",
            "ret":101
        }])

    def test_order(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT])

        tmp = hf.call("order")
        self.assertEqual(tmp,[
            {
                "pkg":"hiframe_test_basic_plugin",
                "module":"_hiframe",
                "class":"HiframeTestBasicPlugin",
                "func":"order_c",
                "ret":"c"
            },
            {
                "pkg":"hiframe_test_basic_plugin",
                "module":"_hiframe",
                "class":"HiframeTestBasicPlugin",
                "func":"order_a",
                "ret":"a"
            },
            {
                "pkg":"hiframe_test_basic_plugin",
                "module":"_hiframe",
                "class":"HiframeTestBasicPlugin",
                "func":"order_b",
                "ret":"b"
            },
        ])

    def test_pkg2(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT])
        tmp = hf.call("pkg2")
        self.assertEqual(tmp,[
            {
                "pkg":"hiframe_test_basic_plugin",
                "module":"_hiframe",
                "class":"HiframeTestBasicPlugin",
                "func":"pkg2_c",
                "ret":"c"
            },
            {
                "pkg":"hiframe_test_basic_plugin2",
                "module":"_hiframe",
                "class":"HiframeTestBasicPlugin2",
                "func":"pkg2_b",
                "ret":"b"
            },
            {
                "pkg":"hiframe_test_basic_plugin",
                "module":"_hiframe",
                "class":"HiframeTestBasicPlugin",
                "func":"pkg2_a",
                "ret":"a"
            },
        ])
        
    def test_no_order(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT])
        tmp = hf.call("no_order")
        self.assertTrue({
            "pkg":"hiframe_test_basic_plugin",
            "module":"_hiframe",
            "class":"HiframeTestBasicPlugin",
            "func":"no_order_a",
            "ret":"a"
        } in tmp)
        self.assertTrue({
            "pkg":"hiframe_test_basic_plugin",
            "module":"_hiframe",
            "class":"HiframeTestBasicPlugin",
            "func":"no_order_b",
            "ret":"b"
        } in tmp)
        self.assertEqual(len(tmp),2)

    def test_abc(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],filename_list=["_abc"])
        tmp = hf.call("abc key")
        self.assertEqual(tmp,[{
            "pkg":"hiframe_test_basic_plugin",
            "module":"_abc",
            "class":"HiframeTestBasicPlugin_ABC",
            "func":"abc_func",
            "ret":"abc ret"
        }])

    def test_not_exist(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT])
        tmp = hf.call("not_exist")
        self.assertEqual(tmp,[])

    def test_get_func_list(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT])

        tmp = hf.get_func_list("order")
        self.assertEqual(tmp,[
            {
                "pkg":"hiframe_test_basic_plugin",
                "module":"_hiframe",
                "class":"HiframeTestBasicPlugin",
                "func":"order_c",
                "call":hiframe_test_basic_plugin._hiframe.HiframeTestBasicPlugin.order_c
            },
            {
                "pkg":"hiframe_test_basic_plugin",
                "module":"_hiframe",
                "class":"HiframeTestBasicPlugin",
                "func":"order_a",
                "call":hiframe_test_basic_plugin._hiframe.HiframeTestBasicPlugin.order_a
            },
            {
                "pkg":"hiframe_test_basic_plugin",
                "module":"_hiframe",
                "class":"HiframeTestBasicPlugin",
                "func":"order_b",
                "call":hiframe_test_basic_plugin._hiframe.HiframeTestBasicPlugin.order_b
            },
        ])
