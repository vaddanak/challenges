# MySQL Connector/Python - MySQL driver written in Python.
# Copyright (c) 2013, 2014, Oracle and/or its affiliates. All rights reserved.

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

import os
import sys
import datetime
import logging

try:
    from argparse import ArgumentParser
except:
    # Python v2.6
    from optparse import OptionParser

# CPYINT/support package can only be loaded and used when it is located in the
# repository root of MySQL Connector/Python (CPY)
_CHECK_FILES = [
    os.path.exists(os.path.join('lib', 'mysql', 'connector')),
    os.path.isfile('setupinfo.py'),
    os.path.isfile('unittests.py'),
    os.path.isdir('cpyint')
]
if not all(_CHECK_FILES):
    raise ImportError(
        "CPYINT metasupport module needs to be loaded from the root "
        "of the MySQL Connector/Python repository.\n"
    )

from cpyint.cpydist import opensource
# Minimum MySQL version we need. This should be the latest version of the
# one after the greatest GA. For example, MySQL 5.5 is GA, but 5.6 is still
# Development, then the minimum version should be the latest of 5.6.
# Set the MYSQL_RELEASED to the date when MIN_MYSQL_VERSION was released.
MIN_MYSQL_VERSION = (5, 7, 5)
MYSQL_RELEASED = datetime.date(2014, 9, 25)
MYSQL_RELEASE_MAXAGE = 120  # days


def check_python_version(v2=None, v3=None):
    unsupported_version = None

    if v2 and sys.version_info[0] == 2:
        if sys.version_info[:2] < (2, 7):
            unsupported_version = v2

    elif v3 and sys.version_info[0] == 3:
        if sys.version_info[:2] < (3, 2):
            unsupported_version = v3
    else:
        print("Python {ver} not supported".format(ver=str(sys.version_info)))

    if unsupported_version:
        print("Python v{ver} or greater is required".format(
            ver='.'.join([str(i) for i in unsupported_version])))
        exit(3)

def get_cli_arguments(args=None, description=None):
    """Parse command line ArgumentParser

    This function parses the command line arguments and returns the options.

    It works with both optparse and argparse where available.
    """
    if not args:
        try:
            args = _CMD_ARGS
        except NameError:
            raise NameError("_CMD_ARGS is not defined in module")

    def _clean_optparse(adict):
        """Remove items from dictionary ending with _optparse"""
        new = {}
        for key in adict.keys():
            if not key.endswith('_optparse'):
                new[key] = adict[key]
        return new

    new = True
    try:
        parser = ArgumentParser(description)
        add = parser.add_argument
    except NameError:
        # Fallback to old optparse
        new = False
        parser = OptionParser()
        add = parser.add_option

    for flags, params in args.items():
        if new:
            flags = [i for i in flags if i]
        add(*flags, **_clean_optparse(params))

    options = parser.parse_args()

    if isinstance(options, tuple):
        # Fallback to old optparse
        return options[0]

    return options


def write_cpy_source_header(fp, version, start_year=None):
    fp.write("# -*- coding: utf-8 -*-\n\n")

    years = []
    if start_year:
        years = [start_year]
    years.append(datetime.datetime.now().year)
    license_ = opensource.GPLGNU2_LICENSE_NOTICE.format(
        year=', '.join([str(i) for i in years]))
    linenr = 0
    for licline in license_.split('\n'):
        linenr += 1
        if linenr == 3 and licline == "":
            fp.write("\n".format(licline))
            continue
        fp.write("# {}\n".format(licline))
    fp.write("\n# This file was auto-generated.\n")

    fp.write("_GENERATED_ON = '{}'\n".format(
        datetime.datetime.now().date()))
    fp.write("_MYSQL_VERSION = ({:d}, {:d}, {:d})\n\n".format(
        *version))


def get_mysql_version_from_source(source):
    """Reads the MySQL version from the source

    This function reads the MySQL version from the source and returns it as
    as tuple: (MAJOR, MINOR, PATCH).

    Returns a tuple.
    """
    fn = os.path.join(source, 'VERSION')
    with open(fn, 'r') as fp:
        lines = fp.readlines()
        version = [int(l.split('=')[1]) for l in lines[0:3]]
    return tuple(version)


def check_execution_location():
    """Check whether this script is exeucted in the correct location

    This function checks wether the script is executed in the correct
    location. This script has to be executed from the root of the
    Connector/Python source.
    """
    if not all(_CHECK_FILES):
        raise RuntimeError


def check_mysql_version(version):
    """Check the given MySQL source location

    This function will check if the given MySQL source is usable. If not, it
    will raise a ValueError exception.
    """
    if version < MIN_MYSQL_VERSION:
        raise ValueError("MySQL v{:d}.{:d}.{:d} is too old".format(*version))


def check_mysql_source(source, checks):
    """Check the given MySQL source location

    This function will check if the given MySQL source is usable. If not, it
    will raise a ValueError exception.
    """
    for location in checks:
        if not os.path.exists(location):
            raise ValueError("File '{}' not available".format(location))


def check_mysql_version_freshness(released=MYSQL_RELEASED):
    """Check whether the release date of minimum MySQL version is valid"""
    days = (datetime.datetime.now().date() - released).days
    logging.debug("Minimum MySQL version is {} days old.".format(days))
    if days > MYSQL_RELEASE_MAXAGE:
        raise ValueError("Minimum MySQL version is older than {} days".format(
            MYSQL_RELEASE_MAXAGE))
