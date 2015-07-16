#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MySQL Connector/Python - MySQL driver written in Python.
# Copyright (c) 2012, 2014, Oracle and/or its affiliates. All rights reserved.

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

"""Parse client and server errors from the MySQL Sources

This module parses MySQL client and server errors from the MySQL sources.
It is used to keep the mysql.connector errcode and locales modules up-to-date.

Important:
* The minimum MySQL version has to be updated in this script to the latest
  development MySQL Server. The script will check when the latest update
  was done and give an error when it is older than MYSQL_RELEASE_MAXAGE days.
  See the MIN_MYSQL_VERSION variable in the script.
* This script only works with Python v2.7 and Python v3.2 (or later).
"""


from __future__ import print_function

import codecs
from collections import OrderedDict
import logging
import os
import re
import sys

sys.path.insert(0, 'lib')
sys.path.insert(0, '.')

from cpyint.metasupport import (
    write_cpy_source_header,
    get_cli_arguments,
    check_python_version,
    check_mysql_version_freshness,
    check_execution_location,
    check_mysql_source,
    get_mysql_version_from_source,
    check_mysql_version,
)

check_python_version(v2=(2, 7), v3=(3, 2))

# File to parse relative to the MySQL source
ERR_SERVER_FILE = os.path.join("sql", "share", "errmsg-utf8.txt")
ERR_CLIENT_HEADER = os.path.join("include", "errmsg.h")
ERR_CLIENT_CFILE = os.path.join("libmysql", "errmsg.c")

# Name of the module which will contain the error codes and messages
ERRCODE_MODULE = 'errorcode.py'
ERRLOCALE_SERVER = 'errors_server.py'
ERRLOCALE_CLIENT = 'errors_client.py'

_ERROR_SERVER = 1
_ERROR_CLIENT = 2

_CMD_ARGS = {
    ('', '--output'): {
        'metavar': 'DIR',
        'help': "Where to write the modules (used for debugging)"
    },
    ('', 'source'): {
         'metavar': 'SOURCE',
        'help': (
            "Location of the latest released MySQL sources.")
    },
    ('', '--language'): {
        'dest': 'language', 'default': 'eng',
        'metavar': 'LANG',
        'help': (
            "Which language to parse and write. Use 'all' for all languages.")
    },
    ('', '--debug'): {
        'dest': 'debug', 'action': 'store_true', 'default': False,
        'help': 'Show/Log debugging messages'
    },
}


class _ParseError(Exception):
    pass


class MySQLErrorsProcessor(object):
    """Parse and write MySQL client and server error messages"""
    def __init__(self, source_path, mysql_version, output_folder):
        self._source_path = source_path
        self._output_folder = output_folder
        self._mysql_version = mysql_version
        self._mysql_version_str = '{:d}.{:d}.{:d}'.format(*mysql_version)
        self._languages = []
        self._errors = OrderedDict()
        self._init_server_errors()
        self._init_client_errors()
        self._lang_count = {}

        self._parse_server_errors()
        self._parse_client_errors()

    def _init_server_errors(self):
        """Initialize the server error parser"""
        txt_file = os.path.join(self._source_path, ERR_SERVER_FILE)
        if not os.path.isfile(txt_file):
            _ParseError(
                "Could not find error messages file under "
                "{}".format(self._source_path)
            )

        logging.debug('Parsing server errors from file {}'.format(txt_file))
        self._server_errmsg_file = txt_file
        self._errors_info = {}

    def _init_client_errors(self):
        """Initialize the client error parser"""
        header_file = os.path.join(self._source_path, ERR_CLIENT_HEADER)
        if not os.path.isfile(header_file):
            _ParseError(
                "Could not find error messages file under "
                "{}".format(self._source_path)
            )

        c_file = os.path.join(self._source_path, ERR_CLIENT_CFILE)
        if not os.path.isfile(c_file):
            _ParseError(
                "Could not find error messages file under "
                "{}".format(self._source_path)
            )

        logging.debug('Parsing client errors from file {}'.format(header_file))
        self._client_errmsg_header = header_file
        self._client_errmsg_cfile = c_file

    def _parse_server_errors(self):
        """Parse server error codes"""
        fp = codecs.open(self._server_errmsg_file, 'r', 'utf8')
        curr_err_name = None
        line_nr = 1
        curr_code = 1000 # will be set reading 'start-error-number'
        self._regex_serverr_msg = None
        for line in fp:
            if line.startswith('#'):
                continue
            elif line.startswith('start-error-number'):
                self._errors_info['offset'] = \
                    self._serverr_error_offset(line)
                curr_code = self._errors_info['offset']
            elif line.startswith(('\t',' ')):
                if not self._regex_serverr_msg:
                    self._regex_serverr_msg = re.compile(r'([\w-]*)\s+"(.*?)"')
                try:
                    lang, msg = self._serverr_message(line)
                except ValueError:
                    raise ValueError("Found problem in line nr %d" % line_nr)
                self._lang_count[lang] = self._lang_count.get(lang, 0) + 1
                self._errors[curr_err_name]['messages'][lang] = msg
                if lang not in self._languages:
                    self._languages.append(lang)
                if lang == '':
                    logging.debug("Empty lang: {}".format(line))
            elif line.startswith(('ER_', 'WARN_')):
                res = self._serverr_string(line)
                curr_err_name = res[0]
                if curr_err_name not in self._errors:
                    self._errors[curr_err_name] = {
                        'sqlcodes': res[1:],
                        'messages': {},
                        'code': curr_code,
                        'type': _ERROR_SERVER,
                        }
                    curr_code += 1
            line_nr += 1
        logging.debug(
            "MySQL v{version} server error messages read, "\
            "last was {last}.".format(
                version=self._mysql_version_str,
                last=curr_code))

        self._regex_serverr_msg = None
        fp.close()

    def get_error_by_number(self, nr):
        """Get information about an error by it's number

        Returns a string and dictionary.
        """
        for errname, err in self._errors.items():
            if err['code'] == nr:
                return errname, err
        return None

    def _parse_client_error_messages(self):
        """Parse client error messages"""
        lang = 'eng'
        fp = codecs.open(self._client_errmsg_cfile)
        with codecs.open(self._client_errmsg_cfile, 'r', 'latin1') as fp:
            found = False
            nr = 2000
            for line in fp:
                line = line.strip()
                if not found:
                    if line == "const char *client_errors[]=":
                        found = True
                    continue

                if line.startswith('"') and line != '""':
                    err_name, err = self.get_error_by_number(nr)
                    message = line.replace('"', '').rstrip(',')
                    self._errors[err_name]['messages'][lang] = message
                    self._lang_count[lang] = self._lang_count.get(lang, 0) + 1
                    nr += 1

    def _parse_client_errors(self):
        """Parse client error codes"""
        fp = codecs.open(self._client_errmsg_header, 'r', 'utf8')

        ignored = (
            '#define CR_MIN_ERROR',
            '#define CR_MAX_ERROR',
            '#define CR_ERROR_FIRST',
            '#define CR_ERROR_LAST'
            )

        err_code = None
        for line in fp:
            if line.startswith(ignored):
                continue
            if line.startswith('#define CR_'):
                err_name, err_code = line.split()[1:3]
                self._errors[err_name] = {
                    'messages': {},
                    'code': int(err_code),
                    'type': _ERROR_CLIENT,
                    }
        logging.debug("Last client error code was {}".format(err_code))

        fp.close()

        self._parse_client_error_messages()

    def _serverr_string(self, line):
        """Parse server error from given line

        This method parsers the given line and returns a tuple containing
        the error code and, if available, also the SQL State information.

        Example line:
            ER_ACCESS_DENIED_ERROR 28000

        Returns a tuple.
        """
        try:
            return line.strip().split()
        except ValueError:
            return (line.strip())

    def _serverr_error_offset(self, line):
        """Parse the offset from which server errors begin

        This method parsers the server error offset and returns it as an
        integer. The value of the offset is most probably 1000.

        Line is usually as follows:
            start-error-number 1000

        """
        errno = int(line.strip().split()[1])
        logging.debug("Server error offset: {:d}".format(errno))
        return errno

    def _serverr_message(self, line):
        """Parse the error message

        This method parses the language and message from the given line and
        returns it as a tuple: (language, message). Values in the tuple are
        unicode.

        Returns a tuple.
        """
        matches = self._regex_serverr_msg.search(line)
        if matches:
            return matches.groups()
        else:
            raise ValueError("Failed reading server error message")

    def _serverr_get_translations(self):
        """Create a dictionary of server codes with translations

        This method will return a dictionary where the key is the server
        error code and value another dictionary containing the error message
        in all available languages.

        Example output:
            { 1003: {
                'eng': "NO",
                'ger': "Nein",
                'kor': "아니오"',
                ...
                }
            }

        String values are unicode.

        Returns a dictionary.
        """
        result = {}
        for err_name, err in self._errors.items():
            result[err['code']] = err['messages']
        return result

    def write_module(self, output_folder=None):
        output_folder = output_folder or self._output_folder

        errcode_module = os.path.join(output_folder, ERRCODE_MODULE)
        logging.debug("Writing error codes to '{}', MySQL v{}".format(
                      errcode_module, self._mysql_version_str))

        fp = codecs.open(errcode_module, 'w', 'utf8')
        write_cpy_source_header(fp, self._mysql_version, start_year=2013)

        fp.write("\"\"\"This module contains the MySQL Server "
            "and Client error codes\"\"\"\n\n")

        fp.write("# Start MySQL Errors\n")
        for err_name, err in self._errors.items():
            fp.write('{0} = {1}\n'.format(err_name, err['code']))

        fp.write("# End MySQL Errors\n\n")

        fp.close()

    def _setup_locales_folder(self, output_folder, language='all'):
        """Setup the folder for storing translations

        This method will setup the folder storing translations using the
        languages found while parsing error messages.

        The folder (package) structure will be as follows:
            <output_folder>/
                locales/
                    __init__.py
                    <language>/
                        __init__.py

        Returns a string.
        """
        if language == 'all':
            languages = self._languages
        else:
            languages = [ language ]

        def create(folder):
            if not os.path.exists(folder):
                os.mkdir(folder)
            init_file = os.path.join(folder, '__init__.py')
            if not os.path.isfile(init_file):
                open(init_file, 'w').close()

        locale_folder = os.path.join(self._output_folder, 'locales')
        create(locale_folder)

        for lang in languages:
            lang_folder = os.path.join(locale_folder,
                                       lang.replace('-','_'))
            create(lang_folder)

        return locale_folder

    def _write_error_messages(self, language, locale_folder,
                              module_name, errtype=None):
        """Write the error messages to a Python module

        This method will write error messages for a certain language into a
        python module locate in the locale_folder. If the errtype is
        given, it will only write message corresponding to a certain error
        type.
        """
        modfile = os.path.join(locale_folder, language.replace('-','_'),
                               module_name)

        logging.debug("Writing error module for {}, ".format(
            modfile, self._mysql_version_str))
        fp = codecs.open(modfile, 'w', 'utf8')
        write_cpy_source_header(fp, self._mysql_version,  start_year=2013)

        fp.write("# Start MySQL Error messages\n")
        for err_name, err in self._errors.items():
            if errtype and err['type'] != errtype:
                continue

            try:
                err_msg = err['messages'][language]
            except KeyError:
                # No translation available
                continue

            err_msg = err_msg.replace('%d', '%s')
            err_msg = err_msg.replace('%lu', '%s')

            fp.write(u'{code} = u"{msg}"\n'.format(code=err_name, msg=err_msg))

        fp.write("# End MySQL Error messages\n\n")
        fp.close()

    def write_locale_errors(self, language='all', output_folder=None):
        """Write the MySQL server error translations to Python module

        This method will write the MySQL server error translations to a
        Python module. If output_folder is given, it will create (or overwrite)
        the module in the given directory. If not given, a subfolder will
        be used (and if needed created) in the Connector/Python source.
        """
        output_folder = output_folder or self._output_folder
        locale_folder = self._setup_locales_folder(output_folder, language)

        if language == 'all':
            languages = self._languages
        else:
            languages = [ language ]

        for lang in languages:
            self._write_error_messages(lang, locale_folder,
                                       'client_error.py', _ERROR_CLIENT)
            #self._write_error_messages(lang, locale_folder,
            #                           'server_error.py', _ERROR_SERVER,)


def main():
    """Start the script"""
    args = get_cli_arguments(_CMD_ARGS, description="mysql_errors.py")
    if not args.source:
        print("--source argument i.e. path to mysql source directory is "
              "required.")
        exit(4)
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    try:
        check_mysql_version_freshness()
        check_execution_location()
    except RuntimeError:
        raise
        print("Execute this script from the root of Connector/Python source")
        exit(3)
    except ValueError as err:
        print("Update script: {}".format(err))
        exit(3)

    mysql_version = ()
    try:
        checks = [
            os.path.join(args.source, ERR_SERVER_FILE),
            os.path.join(args.source, ERR_CLIENT_HEADER),
            os.path.join(args.source, ERR_CLIENT_CFILE),
        ]
        check_mysql_source(args.source, checks)

        mysql_version = get_mysql_version_from_source(args.source)
        check_mysql_version(mysql_version)
    except ValueError as err:
        print("The given MySQL source can not be used: {}".format(err))
        exit(3)
    else:
        logging.debug("Using MySQL v{ver} sources found in {loc}".format(
            ver="{:d}.{:d}.{:d}".format(*mysql_version), loc=args.source))

    output_folder = args.output or os.path.join('lib', 'mysql', 'connector')
    logging.debug("Output folder: {}".format(output_folder))

    try:
        myerrmsgs = MySQLErrorsProcessor(
            args.source, mysql_version, output_folder)
    except _ParseError as err:
        print(err)
        exit(1)
    else:
        myerrmsgs.write_module()
        myerrmsgs.write_locale_errors(language=args.language)


if __name__ == '__main__':
    main()


