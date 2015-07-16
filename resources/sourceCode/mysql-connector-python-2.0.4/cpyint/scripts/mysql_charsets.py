# MySQL Connector/Python - MySQL driver written in Python.
# Copyright (c) 2013, 2014, Oracle and/or its affiliates. All rights reserved.

# MySQL Connector/Python is licensed under the terms of the GPLv2
# <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>, like most
# MySQL Connectors. There are special exceptions to the terms and
# conditions of the GPLv2 as it is applied to this software, see the
# FOSS License Exception
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


"""Parse MySQL supported Character Sets and Collations
"""

import codecs
import logging
import os
import sys

sys.path.insert(0, 'lib')
sys.path.insert(0, '.')

import mysql.connector
from cpyint.metasupport import (
    MIN_MYSQL_VERSION,
    check_python_version,
    check_mysql_version,
    check_mysql_version_freshness,
    get_cli_arguments,
    write_cpy_source_header,
)

check_python_version(v2=(2, 7), v3=(3, 2))

# Name of the module which will contain the character sets
CHARSET_MODULE = 'charsets.py'

# Default database configuration
_DB_CONFIG = {
    'user': 'root',
    'password': '',
    'database': 'INFORMATION_SCHEMA',
    'host': '127.0.0.1',
    'port': 3306,
    'unix_socket': None,
}

_CMD_ARGS = {
    ('', '--output'): {
        'metavar': 'DIR',
        'help': "Where to write the modules (used for debugging)"
    },
    ('', '--host'): {
        'dest': 'host', 'default': _DB_CONFIG['host'], 'metavar': 'NAME',
        'help': (
            "MySQL server for retrieving character set information. Must be "
            "version {0}.{1}.{2}.").format(*MIN_MYSQL_VERSION)
    },
    ('', '--port'): {
        'dest': 'port', 'default': _DB_CONFIG['port'], 'metavar': 'PORT',
        'help': (
            "TCP/IP port of the MySQL server")
    },

    ('', '--user'): {
        'dest': 'user', 'default': _DB_CONFIG['user'], 'metavar': 'NAME',
        'help': (
            "User for connecting with the MySQL server")
    },

    ('', '--password'): {
        'dest': 'password', 'default': _DB_CONFIG['password'],
        'metavar': 'PASSWORD',
        'help': (
            "Password for connecting with the MySQL server")
    },
    ('-S', '--socket'): {
        'dest': 'unix_socket', 'default': _DB_CONFIG['unix_socket'],
        'metavar': 'NAME',
        'help': "Socket file for connecting with the MySQL server"
    },
    ('', '--debug'): {
        'dest': 'debug', 'action': 'store_true', 'default': False,
        'help': 'Show/Log debugging messages'
    },
}


def write_module(version, output_folder=None, dbconfig=None):
    """Write the module"""
    if not dbconfig:
        dbconfig = _DB_CONFIG.copy()

    output_folder = output_folder

    charset_module = os.path.join(output_folder, CHARSET_MODULE)
    logging.debug("Writing character sets to '{}'".format(
                  charset_module))

    fp = codecs.open(charset_module, 'w', 'utf8')
    write_cpy_source_header(fp, version, start_year=2013)

    cnx = mysql.connector.connect(**dbconfig)
    cur = cnx.cursor()

    cur.execute(
        "SELECT id, character_set_name, collation_name, is_default "
        "FROM collations ORDER BY id"
    )

    fp.write('"""This module contains the MySQL Server Character Sets"""\n\n')

    fp.write('MYSQL_CHARACTER_SETS = [\n')
    fp.write('    # (character set name, collation, default)\n')
    prev_id = 0
    for (id, charset, collation, default) in cur:
        for i in range(id - prev_id):
            fp.write('    None,\n')
        if default == 'Yes':
            default = 'True'
        else:
            default = 'False'
        fp.write('    ("{0}", "{1}", {2}),  # {3}\n'.format(
                 charset, collation, default, id))
        prev_id = id + 1
    fp.write("]\n\n")
    print("Wrote {0}".format(charset_module))

    cnx.close()
    fp.close()


def main():
    """Start the script"""
    args = get_cli_arguments(
        _CMD_ARGS, description="mysql_charsets")
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    try:
        check_mysql_version_freshness()
    except ValueError as err:
        print("Update script: {}".format(err))
        exit(3)

    config = _DB_CONFIG.copy()
    config['host'] = args.host
    config['port'] = args.port
    config['user'] = args.user
    config['password'] = args.password
    config['unix_socket'] = args.unix_socket

    mysql_version = (99, 9, 9)
    try:
        cnx = mysql.connector.connect(**config)
        mysql_version = cnx.get_server_version()
        cnx.close()
        check_mysql_version(mysql_version)
    except mysql.connector.Error as exc:
        print("Failed connecting to MySQL server: {error}".format(
            error=str(exc)))
        exit(3)
    except ValueError as err:
        print("The given MySQL server can not be used: {}".format(err))
        exit(3)
    else:
        logging.debug("Using MySQL v{ver}".format(
            ver="{:d}.{:d}.{:d}".format(*mysql_version)))

    if args.output:
        output_folder = args.output
    else:
        output_folder = os.path.join('lib', 'mysql', 'connector')

    write_module(mysql_version, output_folder, config)

if __name__ == '__main__':
    main()
