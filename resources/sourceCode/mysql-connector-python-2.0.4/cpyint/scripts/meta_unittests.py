# MySQL Connector/Python - MySQL driver written in Python.
# Copyright (c) 2013, 2015, Oracle and/or its affiliates. All rights reserved.

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
"""Running tests checking sources and distribution

This script should be executed from the root of the MySQL Connector/Python
source code.
 shell> python support/tests/run.py
"""


import argparse
import re
import subprocess
import sys

try:
    from docutils.core import publish_doctree
except ImportError:
    raise ImportError("docutils is required for running internal tests")

sys.path.insert(0, 'lib')
sys.path.insert(0, '.')

from cpyint.metasupport import (
    check_python_version
)
from cpyint.metasupport import tests

check_python_version(v2=(2, 7), v3=(3, 3))


def parse_version(verstr):
    """Parses the Connector/Python version string

    Returns a tuple, or None.
    """
    # Based on regular expression found in PEP-386
    expr = (r'^(?P<version>\d+\.\d+)(?P<extraversion>(?:\.\d+){1})'
            r'(?:(?P<prerel>[ab])(?P<prerelversion>\d+(?:\.\d+)*))?$')
    re_match = re.match(expr, verstr)

    if not re_match:
        return None

    info = [ int(val) for val in re_match.group('version').split('.') ]
    info.append(int(re_match.group('extraversion').replace('.', '')))
    info.extend(['', 0])
    try:
        info[3] = re_match.group('prerel') or ''
        info[4] = int(re_match.group('prerelversion'))
    except TypeError:
        # It's OK when this information is missing, check happend earlier
        pass
    return tuple(info)


def main():
    """Run tests"""
    argparser = argparse.ArgumentParser(
        description="Run MySQL Connector/Python tests "
                    "checking sources and distribution.")
    argparser.add_argument(
        '--connector-version', type=str,
        dest='connector_version', action='store', required=True,
        help="Current version of MySQL Connector/Python")

    try:
        subprocess.check_output(['git', 'version'])
    except OSError:
        sys.stderr.write("Git not available. Make sure git is in your PATH.\n")
        sys.exit(1)

    args = argparser.parse_args()
    tests.CHECK_CPY_VERSION = parse_version(args.connector_version)
    if not tests.CHECK_CPY_VERSION:
        sys.stderr.write("'{ver}' is not a valid version "
                         "for MySQL Connector/Python.\n".format(
                            ver=args.connector_version))
        sys.exit(1)

    tests.run()


if __name__ == '__main__':
    main()

