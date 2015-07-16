#!/usr/bin/env python
# -*- coding: utf-8 -*-
# MySQL Connector/Python - MySQL driver written in Python.
# Copyright (c) 2013, 2014 Oracle and/or its affiliates. All rights reserved.

"""Run the unittests.py against various Python and MySQL versions

This script requires Python v2.7 or later. For additional information
see the output of the --help argument:

 shell> python unittest_run.py --help

Usually, this script is executed in the source code of Connector/Python,
for example, when in the root of the source:

 shell> python ./support/scripts/unittest_run.py -p 2.7 -p 2.6

unittest_run.py will detect which Python versions to run the unit tests
with using the version.py of Connector/Python.

The Python versions are supposed to be installed in /opt/python/X.Y, where
X.Y is something like 2.6 or 3.2.
"""


import argparse
import logging
import os
import re
import subprocess
import sys

DESCPRIPTION = "Run unittest.py for specified Python versions"
PYVER = {
    '2.0': ('2.6', '2.7', '3.3', '3.4'),
    '1.1': ('2.6', '2.7', '3.1', '3.2', '3.3', '3.4'),
    '1.1': ('2.6', '2.7', '3.1', '3.2', '3.3', '3.4'),
    '1.0': ('2.4', '2.5', '2.6', '2.7', '3.1', '3.2', '3.3'),
    }

log = logging.getLogger(os.path.basename(__file__))


class TestPythonError(Exception):
    pass


def get_version_connector(source):

    VERSION = [999, 0, 0, 'a', 0]  # Set correct after version.py is loaded

    # 1.x location
    versionpy_1x = os.path.join(source, 'version.py')
    # 2.x location
    versionpy_2x = os.path.join(source, 'lib',
                                'mysql', 'connector', 'version.py')

    if os.path.exists(versionpy_1x):
        version_py = versionpy_1x
    else:
        version_py = versionpy_2x

    with open(version_py, 'rb') as fp:
        exec(compile(fp.read(), version_py, 'exec'))

    return VERSION

def get_mysql_version(mysqld_path):
    """Get the MySQL server version

    This method executes mysqld with the --version argument. It parses
    the output looking for the version number and returns it as a
    tuple with integer values: (major, minor, patch)

    Returns a tuple.
    """
    cmd = [mysqld_path, '--version']

    DEVNULL = open(os.devnull, 'w')
    prc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=DEVNULL)
    verstr = str(prc.communicate()[0])
    matches = re.match(r'.*Ver (\d)\.(\d).(\d{1,2}).*', verstr)
    try:
        DEVNULL.close()
    except:
        pass

    if matches:
        return tuple([int(v) for v in matches.groups()])
    else:
        raise Exception('Failed reading version from mysqld --version')

def set_python_versions(args):
    try:
        conn_version = get_version_connector(args.source)
    except ImportError:
        log.error("Failed getting Connector/Python version.\n")
        sys.exit(1)
    ver = '.'.join([ str(i) for i in conn_version[0:2]])
    if ver not in PYVER:
        log.error("Version %s is not configured. Fix this script.", ver)
    else:
        args.python_versions = PYVER[ver]

def get_args():
    parser = argparse.ArgumentParser(description=DESCPRIPTION)
    parser.add_argument(
        'source', metavar='source', type=str, nargs='?',
        default=os.getcwd(),
        help=("Location of MySQL Connector/Python source (default: current"
              " working directory)")
        )

    default = '/opt/python'
    parser.add_argument(
        '--python-root', metavar='folder', type=str, dest='python_root',
        default=default,
        help=("Location of Python installations (default: {})".format(default))
        )

    default = '/usr/local/mysql'
    parser.add_argument(
        '--with-mysql', metavar='folder', type=str, dest='mysql_base',
        default=default,
        help=("Location of MySQL server installation (default: {}".format(
            default))
        )

    parser.add_argument(
        '-p', metavar='version',
        dest='python_versions', action='append',
        default=None,
        help=("Which Python version to test, repeat option to test"
              " multiple versions (default: depending on Connector/Python"
              " version)")
        )

    parser.add_argument(
        '--no-log',
        dest='no_log', action='store_true',
        help="Do not write log files")

    default = 0
    parser.add_argument(
        '--verbose', metavar='level', type=int,
        dest='verbose',
        default=0,
        help="Verbosity level passed to unittests.py (default: {})".format(
            default))

    args = parser.parse_args()
    if not args.python_versions:
        set_python_versions(args)
    return args

def run_unittestpy(pyver, myver, args):
    if pyver.startswith('3'):
        pyexe = 'python3'
    else:
        pyexe = 'python'
    logname = 'tests_{pyver}_{myver}.log'.format(pyver=pyver, myver=myver)

    if not args.no_log:
        log.info("Writing logfile '{}'".format(logname))

    cmd = [
        os.path.join(args.python_root, pyver, 'bin', pyexe),
        'unittests.py',
        '--force',
        '--with-mysql', args.mysql_base,
        '--verbosity', str(args.verbose),
        ]

    conn_version = get_version_connector(args.source)

    if conn_version >= (1, 1):
        cmd.append('--stats')

    proc = subprocess.Popen(cmd, shell=False,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT,
                            universal_newlines=True
                            )
    stdout, stderr = proc.communicate()
    if not args.no_log:
        with open(logname, 'w') as fp:
            fp.write(stdout)

    return proc.returncode

def check_availability_python(pyver, python_root):
    if pyver.startswith('3'):
        pyexe = 'python3'
    else:
        pyexe = 'python'
    cmd = os.path.join(python_root, pyver, 'bin', pyexe)
    if os.path.isfile(cmd) and os.access(cmd, os.X_OK):
        return

    raise TestPythonError(
        "Python {version} not available under '{path}'".format(
            version=pyver, path=os.path.join(python_root, pyver))
        )

def check_availability_mysql(mysql_base):
    cmds = [
        os.path.join(mysql_base, 'bin', 'mysqld'),
        os.path.join(mysql_base, 'libexec', 'mysqld')
        ]
    for cmd in cmds:
        if os.path.isfile(cmd) and os.access(cmd, os.X_OK):
            return get_mysql_version(cmd)

    raise TestPythonError(
        "MySQL executable mysqld not found under '{path}'".format(
            path=mysql_base)
        )

def main():
    args = get_args()
    logfmt = logging.Formatter(
        "%(asctime)s [%(name)s:%(levelname)s] %(message)s")
    loghandle = logging.StreamHandler()
    loghandle.setFormatter(logfmt)
    log.addHandler(loghandle)
    log.setLevel(logging.INFO)

    for pyver in args.python_versions:
        try:
            check_availability_python(pyver, args.python_root)
        except TestPythonError as err:
            log.error(str(err) + '\n')
            sys.exit(1)
    log.info(
        "Testing Python version{} {}".format(
            's' if len(args.python_versions) > 1 else '',
            ', '.join(args.python_versions)))

    mysql_version = check_availability_mysql(args.mysql_base)
    for pyver in args.python_versions:
        myver = '.'.join([str(i) for i in mysql_version[0:2]])
        log.info("Using MySQL Installation from '{}'".format(args.mysql_base))
        versions = "Python v{pyver} and MySQL v{myver}".format(
            pyver=pyver, myver=myver
        )
        log.info("Starting tests using %s", versions)
        rc = run_unittestpy(pyver, myver, args)
        if rc:
            log.error("%s unittests.py failed, returncode %d", versions, rc)
        else:
            log.info("%s unittests.py successful", versions)

if __name__ == '__main__':
    main()

