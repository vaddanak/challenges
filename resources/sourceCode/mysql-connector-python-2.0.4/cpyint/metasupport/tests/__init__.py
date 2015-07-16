# MySQL Connector/Python - MySQL driver written in Python.
# Copyright (c) 2009, 2013, Oracle and/or its affiliates. All rights reserved.

# MySQL Connector/Python is licensed under the terms of the GPLv2
# <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>, like most
# MySQL Connectors. There are special exceptions to the terms and
# conditions of the GPLv2 as it is applied to this software, see the
# FLOSS License Exception
# <http://www.mysql.com/about/legal/licensing/foss-exception.html>.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA


import logging
import unittest

try:
    import setupinfo
except ImportError:
    raise ImportError("CPYINT tests needs to be executed from the root of the "
                      "MySQL Connector/Python repository.")

__all__ = [
    'run',
    'MySQLConnectorTests',
]

ACTIVE_TESTS = [
    'cpyint.metasupport.tests.test_distribution',
    'cpyint.metasupport.tests.test_version',
    'cpyint.metasupport.tests.test_errorcode'
]

LOGGER_NAME = "myconnpy_support_tests"
CHECK_CPY_VERSION = None  # set by scripts/meta_inittests.py


class SupportTests(unittest.TestCase):

    def get_connector_version(self):
        return setupinfo.VERSION

    def get_connector_version_text(self, suffix=False):
        ver = setupinfo.VERSION
        if not suffix or not (ver[3] and ver[4]):
            return '{0}.{1}.{2}'.format(*ver[0:3])
        else:
            return '{0}.{1}.{2}{3}{4}'.format(*ver)


def run():
    # Enabling logging
    formatter = logging.Formatter("%(asctime)s [%(name)s:%(levelname)s] %(message)s")
    log = logging.getLogger('myconnpy_support')
    fh = logging.StreamHandler()
    fh.setFormatter(formatter)
    log.addHandler(fh)
    log.setLevel(logging.DEBUG)
    log.addHandler(fh)
    log.info("MySQL Connector/Python CPYINT meta unit testing started")
    
    testsuite = unittest.TestLoader().loadTestsFromNames(ACTIVE_TESTS)
    log.info("Starting unit tests")
    
    successful = False
    try:
        # Run test cases
        result = unittest.TextTestRunner().run(testsuite)
        successful = result.wasSuccessful()
    except KeyboardInterrupt:
        log.info("Unittesting was interrupted")
        successful = False

    log.info("Unittesting was%s succesful" % ('' if successful else ' not'))
