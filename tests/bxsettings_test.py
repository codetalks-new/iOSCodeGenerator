import unittest

import os
import sys
sys.path.insert(0, os.path.basename('..'))

from cStringIO import StringIO
from ios_code_generator import bxuimodel_core as core


class MyTestCase(unittest.TestCase):
    def test_settings(self):
        strio = StringIO(u"-AppUserDefaults(sync_on_save=true,prefix=zjjj)\n loveMe:b;count:i;name:s;created:d;avatar:u")
        sys.stdin = strio
        text = core.generate('settings')
        print(text)



if __name__ == '__main__':
    unittest.main()
