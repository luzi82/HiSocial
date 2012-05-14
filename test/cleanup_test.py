import _testcommon
from hisocial.common.Cleanup import Cleanup

class Dummy(object):

    x_count=0

    def x(self):
        self.x_count+=1

class CleanupTest(_testcommon.HsTest):
    
    def test_cleanup(self):
        cl = Cleanup()
        
        d = Dummy()
        cl.push(d.x)
        cl.clean()
        self.assertEqual(d.x_count,1)

    def test_cleanall(self):
        cl = Cleanup()
        
        d = Dummy()
        cl.push(d.x)
        cl.push(d.x)
        cl.clean_all()
        self.assertEqual(d.x_count,2)

    def test_double(self):
        cl0 = Cleanup()
        cl1 = Cleanup()
        
        a0 = Dummy()
        a1 = Dummy()
        
        cl0.push(a0.x)
        self.assertEqual(a0.x_count,0)
        self.assertEqual(a1.x_count,0)
        
        cl1.push(a1.x)
        self.assertEqual(a0.x_count,0)
        self.assertEqual(a1.x_count,0)

        cl1.clean_all()
        self.assertEqual(a0.x_count,0)
        self.assertEqual(a1.x_count,1)

        cl0.clean()
        self.assertEqual(a0.x_count,1)
        self.assertEqual(a1.x_count,1)
