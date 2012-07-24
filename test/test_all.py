import unittest.case
import types
import os
import sys

MY_ABSOLUTE_PATH = os.path.abspath(__file__)
PROJECT_PATH = os.path.dirname(os.path.dirname(MY_ABSOLUTE_PATH))

def deep_test(path,root):
    for m_name in os.listdir(path):
        full_name=path+"/"+m_name
        if full_name == MY_ABSOLUTE_PATH: continue # ignore this file
        if os.path.isdir(full_name):
            if root == "": root2 = m_name
            else: root2 = root+"."+m_name
            deep_test(full_name,root2)
        elif m_name.endswith(".py"):
            if root == "": m_name2 = m_name[:-3]
            else: root2 = m_name2 = root+"."+m_name[:-3]
            if not "test" in m_name2: continue
            m = __import__(name=m_name2)
            attr_list = dir(m)
            for attr in attr_list:
                c = getattr(m,attr)
                if not isinstance(c,types.TypeType): continue
                if not issubclass(c,unittest.case.TestCase): continue
                globals()[attr] = c

test_done = []
for path in sys.path:
    if not path.startswith(PROJECT_PATH+"/"): continue
    if path in test_done: continue
    test_done.append(path)
    deep_test(path,"")
