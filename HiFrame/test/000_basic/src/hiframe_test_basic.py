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
        self.assertEqual(tmp["hiframe_test_basic_plugin"]["module_name"], "_hiframe")
        self.assertEqual(tmp["hiframe_test_basic_plugin"]["class_name"], "HiframeTestBasicPlugin")
        self.assertTrue(isinstance(tmp["hiframe_test_basic_plugin"]["obj"], hiframe_test_basic_plugin._hiframe.HiframeTestBasicPlugin))
        
    def test_scan_func(self):
        plugin_list = hiframe._scan_plugin(plugin_path_list=[MY_ABSOLUTE_PARENT],filename_list=["_hiframe"],hf=None)

        tmp = hiframe._scan_func(plugin_list=plugin_list)
        self.assertEqual(tmp["simple"][0]["func"], plugin_list["hiframe_test_basic_plugin"]["obj"].simple_func)
        self.assertEqual(tmp["simple"][0]["pkg_name"], "hiframe_test_basic_plugin")
        self.assertEqual(tmp["simple"][0]["module_name"], "_hiframe")
        self.assertEqual(tmp["simple"][0]["class_name"], "HiframeTestBasicPlugin")
        self.assertTrue(isinstance(tmp["simple"][0]["obj"], hiframe_test_basic_plugin._hiframe.HiframeTestBasicPlugin))
        self.assertEqual(tmp["simple"][0]["func_name"], "simple_func")
        
    def test_call(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT])
        tmp = hf.call("simple")
        self.assertEqual(tmp,[{
            "pkg_name":"hiframe_test_basic_plugin",
            "module_name":"_hiframe",
            "class_name":"HiframeTestBasicPlugin",
            "func_name":"simple_func",
            "ret":"simple ret"
        }])
        tmp = hf.call("simple_arg",args={"abc":100})
        self.assertEqual(tmp,[{
            "pkg_name":"hiframe_test_basic_plugin",
            "module_name":"_hiframe",
            "class_name":"HiframeTestBasicPlugin",
            "func_name":"simple_arg_func",
            "ret":101
        }])

    def test_order(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT])

        tmp = hf.call("order")
        self.assertEqual(tmp,[
            {
                "pkg_name":"hiframe_test_basic_plugin",
                "module_name":"_hiframe",
                "class_name":"HiframeTestBasicPlugin",
                "func_name":"order_c",
                "ret":"c"
            },
            {
                "pkg_name":"hiframe_test_basic_plugin",
                "module_name":"_hiframe",
                "class_name":"HiframeTestBasicPlugin",
                "func_name":"order_a",
                "ret":"a"
            },
            {
                "pkg_name":"hiframe_test_basic_plugin",
                "module_name":"_hiframe",
                "class_name":"HiframeTestBasicPlugin",
                "func_name":"order_b",
                "ret":"b"
            },
        ])

    def test_pkg2(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT])
        tmp = hf.call("pkg2")
        self.assertEqual(tmp,[
            {
                "pkg_name":"hiframe_test_basic_plugin",
                "module_name":"_hiframe",
                "class_name":"HiframeTestBasicPlugin",
                "func_name":"pkg2_c",
                "ret":"c"
            },
            {
                "pkg_name":"hiframe_test_basic_plugin2",
                "module_name":"_hiframe",
                "class_name":"HiframeTestBasicPlugin2",
                "func_name":"pkg2_b",
                "ret":"b"
            },
            {
                "pkg_name":"hiframe_test_basic_plugin",
                "module_name":"_hiframe",
                "class_name":"HiframeTestBasicPlugin",
                "func_name":"pkg2_a",
                "ret":"a"
            },
        ])
        
    def test_no_order(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT])
        tmp = hf.call("no_order")
        self.assertTrue({
            "pkg_name":"hiframe_test_basic_plugin",
            "module_name":"_hiframe",
            "class_name":"HiframeTestBasicPlugin",
            "func_name":"no_order_a",
            "ret":"a"
        } in tmp)
        self.assertTrue({
            "pkg_name":"hiframe_test_basic_plugin",
            "module_name":"_hiframe",
            "class_name":"HiframeTestBasicPlugin",
            "func_name":"no_order_b",
            "ret":"b"
        } in tmp)
        self.assertEqual(len(tmp),2)

    def test_abc(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],filename_list=["_abc"])
        tmp = hf.call("abc key")
        self.assertEqual(tmp,[{
            "pkg_name":"hiframe_test_basic_plugin",
            "module_name":"_abc",
            "class_name":"HiframeTestBasicPlugin_ABC",
            "func_name":"abc_func",
            "ret":"abc ret"
        }])

    def test_not_exist(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT])
        tmp = hf.call("not_exist")
        self.assertEqual(tmp,[])

    def test_get_func_list(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT])
        
        me = hf.plugin_D["hiframe_test_basic_plugin"]

        tmp = hf.get_func_list("order")
        self.assertEqual(tmp,[
            {
                "pkg_name":"hiframe_test_basic_plugin",
                "module_name":"_hiframe",
                "class_name":"HiframeTestBasicPlugin",
                "func_name":"order_c",
                "func":me.order_c
            },
            {
                "pkg_name":"hiframe_test_basic_plugin",
                "module_name":"_hiframe",
                "class_name":"HiframeTestBasicPlugin",
                "func_name":"order_a",
                "func":me.order_a
            },
            {
                "pkg_name":"hiframe_test_basic_plugin",
                "module_name":"_hiframe",
                "class_name":"HiframeTestBasicPlugin",
                "func_name":"order_b",
                "func":me.order_b
            },
        ])
