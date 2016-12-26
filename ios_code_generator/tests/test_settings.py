import sys

from StringIO import StringIO
from ios_code_generator import generators

def test_settings():
    strio = StringIO(u"""
    -AppUserDefaults(sync_on_save=true,prefix=app)
    loveMe:b;count:i;name:s;created:d;avatar
    """)
    sys.stdin = strio
    text = generators.generate_v2('settings')
    print(text)

def test_no_model():
    strio = StringIO(u"""
    loveMe:b;count:i;name:s;created:d;avatar
    """)
    sys.stdin = strio
    text = generators.generate_v2('settings')
    print(text)

