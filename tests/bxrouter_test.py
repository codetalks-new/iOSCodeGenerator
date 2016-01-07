import unittest

import os
import sys
sys.path.insert(0, os.path.basename('..'))

from ios_code_generator import bxrouter
from cStringIO import StringIO


class MyTestCase(unittest.TestCase):
    def test_bxrouter(self):
        strio = StringIO(u"api/product/isuser_product?id=24351:p;api/product/addUserProduct?id=24351;/api/explore/explore_list?categoryId=&page=&size=10&exploreType=&title=\napi/baike?id=101(p);api/discover/commect_updo/id/47:p")
        sys.stdin = strio
        bxrouter.main()


if __name__ == '__main__':
    unittest.main()
