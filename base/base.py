import unittest

from common.SendRequests import HttpRequests
from common.RecordLog import log

class Base(unittest.TestCase):
    """用例入口"""
    @classmethod
    def setUpClass(cls):
        cls.request = HttpRequests()
        log.info('------开始执行{}测试用例------'.format(cls.__doc__))


    @classmethod
    def tearDownClass(cls):
        cls.request.close_session()
        log.info('------{}测试用例执行结束------'.format(cls.__doc__))

if __name__ == "__main__":
    unittest.main()