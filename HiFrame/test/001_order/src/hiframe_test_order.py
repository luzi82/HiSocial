import unittest
from hiframe import hiframe
import os

MY_ABSOLUTE_PATH = os.path.abspath(__file__)
MY_ABSOLUTE_PARENT = os.path.dirname(MY_ABSOLUTE_PATH)

class HiframeTestBasic(unittest.TestCase):

    def test_after_abc(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT])

        tmp = hf.call("after_abc")
        self.assertEqual(len(tmp),3)
        self.assertEqual(tmp[0]["func"],"after_abc_aaa")
        self.assertEqual(tmp[1]["func"],"after_abc_bbb")
        self.assertEqual(tmp[2]["func"],"after_abc_ccc")

    def test_after_cba(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT])

        tmp = hf.call("after_cba")
        self.assertEqual(len(tmp),3)
        self.assertEqual(tmp[0]["func"],"after_cba_ccc")
        self.assertEqual(tmp[1]["func"],"after_cba_bbb")
        self.assertEqual(tmp[2]["func"],"after_cba_aaa")

    def test_after2(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT])

        tmp = hf.call("after2")
        self.assertEqual(len(tmp),3)
        self.assertEqual(tmp[2]["func"],"after2_bbb")

    def test_before_abc(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT])

        tmp = hf.call("before_abc")
        self.assertEqual(len(tmp),3)
        self.assertEqual(tmp[0]["func"],"before_abc_aaa")
        self.assertEqual(tmp[1]["func"],"before_abc_bbb")
        self.assertEqual(tmp[2]["func"],"before_abc_ccc")

    def test_before_cba(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT])

        tmp = hf.call("before_cba")
        self.assertEqual(len(tmp),3)
        self.assertEqual(tmp[0]["func"],"before_cba_ccc")
        self.assertEqual(tmp[1]["func"],"before_cba_bbb")
        self.assertEqual(tmp[2]["func"],"before_cba_aaa")

    def test_before2(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT])

        tmp = hf.call("before2")
        self.assertEqual(len(tmp),3)
        self.assertEqual(tmp[0]["func"],"before2_bbb")

    def test_afterbefore_abc(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT])

        tmp = hf.call("afterbefore_abc")
        self.assertEqual(len(tmp),3)
        self.assertEqual(tmp[0]["func"],"afterbefore_abc_aaa")
        self.assertEqual(tmp[1]["func"],"afterbefore_abc_bbb")
        self.assertEqual(tmp[2]["func"],"afterbefore_abc_ccc")

    def test_afterbefore_cba(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT])

        tmp = hf.call("afterbefore_cba")
        self.assertEqual(len(tmp),3)
        self.assertEqual(tmp[0]["func"],"afterbefore_cba_ccc")
        self.assertEqual(tmp[1]["func"],"afterbefore_cba_bbb")
        self.assertEqual(tmp[2]["func"],"afterbefore_cba_aaa")

    def test_order_afterbefore_mix_cba(self):
        hf = hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT])

        tmp = hf.call("order_afterbefore_mix_cba")
        self.assertEqual(len(tmp),3)
        self.assertEqual(tmp[0]["func"],"order_afterbefore_mix_cba_ccc")
        self.assertEqual(tmp[1]["func"],"order_afterbefore_mix_cba_bbb")
        self.assertEqual(tmp[2]["func"],"order_afterbefore_mix_cba_aaa")

    def test_contra_a(self):
        try:
            hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],filename="_contra_a")
            self.fail()
        except hiframe.BadFuncKeyException:
            pass

    def test_contra_b(self):
        try:
            hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],filename="_contra_b")
            self.fail()
        except hiframe.BadFuncKeyException:
            pass

    def test_bad_id_a(self):
        try:
            hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],filename="_bad_id_a")
            self.fail()
        except hiframe.BadFuncKeyException:
            pass

    def test_bad_id_b(self):
        try:
            hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],filename="_bad_id_b")
            self.fail()
        except hiframe.BadFuncKeyException:
            pass

    def test_bad_after_0(self):
        try:
            hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],filename="_bad_after_0")
            self.fail()
        except hiframe.BadFuncKeyException:
            pass

    def test_bad_after_1(self):
        try:
            hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],filename="_bad_after_1")
            self.fail()
        except hiframe.BadFuncKeyException:
            pass

    def test_bad_before_0(self):
        try:
            hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],filename="_bad_before_0")
            self.fail()
        except hiframe.BadFuncKeyException:
            pass

    def test_bad_before_1(self):
        try:
            hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],filename="_bad_before_1")
            self.fail()
        except hiframe.BadFuncKeyException:
            pass

    def test_bad_order(self):
        try:
            hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],filename="_bad_order")
            self.fail()
        except hiframe.BadFuncKeyException:
            pass

    def test_not_exist_after(self):
        try:
            hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],filename="_not_exist_after")
            self.fail()
        except hiframe.BadFuncKeyException:
            pass

    def test_not_exist_before(self):
        try:
            hiframe.HiFrame(plugin_path_list=[MY_ABSOLUTE_PARENT],filename="_not_exist_before")
            self.fail()
        except hiframe.BadFuncKeyException:
            pass
