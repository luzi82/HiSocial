import _testcommon
import core_config

class ConfigTest(_testcommon.HsTest):
    
    def test_test_enabled(self):
        self.assertTrue(hasattr(core_config,"TEST_KEY"))
        self.assertNotEqual(core_config.TEST_KEY, None)
        self.assertTrue(isinstance(core_config.TEST_KEY,str))
        self.assertEqual(len(core_config.TEST_KEY), 64)
