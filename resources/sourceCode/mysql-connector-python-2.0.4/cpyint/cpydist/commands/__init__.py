

import os
import sys


VERSION = [999, 0, 0, 'a', 0]  # Set correct after version.py is loaded
EDITION = 'CPYINT'
ARCH_64BIT = sys.maxsize > 2**32

# Try setting VERSION, VERSION_TEXT and EDITION from version.py found in CPY
version_py = os.path.join('lib', 'mysql', 'connector', 'version.py')
try:
    with open(version_py, 'rb') as fp:
        exec(compile(fp.read(), version_py, 'exec'))
except IOError:
    # We are not in CPY repository
    pass
else:
    if VERSION[3] and VERSION[4]:
        VERSION_TEXT = '{0}.{1}.{2}{3}{4}'.format(*VERSION)
    else:
        VERSION_TEXT = '{0}.{1}.{2}'.format(*VERSION[0:3])
    VERSION_TEXT_SHORT = '{0}.{1}.{2}'.format(*VERSION[0:3])

COMMON_USER_OPTIONS = [
    ('edition=', None,
     "Edition added in the package name after the version"),
]

CEXT_OPTIONS = [
    ('with-mysql-capi=', None,
     "Location of MySQL C API installation or path to mysql_config"),
]