import unittest

from VirtualEnvViewer.MD5Generator import md5
from VirtualObject import VirtualObject


class MyTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_equality(self):
        vo1 = VirtualObject([[1,1,1]])
        vo2 = VirtualObject([[1,1,1]])

        self.assertEqual(vo1, vo2)

    def test_hash(self):
        vo1 = VirtualObject([[1,1,1]])
        vo2 = VirtualObject([[1,1,1]])

        self.assertEquals(vo1.__hash__(), vo2.__hash__())



if __name__ == '__main__':
    unittest.main()
