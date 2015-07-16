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
"""Testing error code generation information"""


from datetime import datetime

from lib.mysql.connector import errorcode
from cpyint.metasupport.tests import SupportTests


class ErrorCodeTests(SupportTests):

    def test__GENERATED_ON(self):
        self.assertTrue(isinstance(errorcode._GENERATED_ON, str))
        try:
            generatedon = datetime.strptime(errorcode._GENERATED_ON,
                                            '%Y-%m-%d').date()
        except ValueError as err:
            self.fail(err)

        delta = (datetime.now().date() - generatedon).days
        self.assertTrue(
            delta < 120,
            "errorcode.py is more than 120 days old ({0})".format(delta))


class LocalesEngClientErrorTests(SupportTests):

    """Testing locales.eng.client_error"""

    def test__GENERATED_ON(self):
        try:
            from lib.mysql.connector.locales.eng import client_error
        except ImportError:
            self.fail("locales.eng.client_error could not be imported")

        self.assertTrue(isinstance(client_error._GENERATED_ON, str))
        try:
            generatedon = datetime.strptime(client_error._GENERATED_ON,
                                            '%Y-%m-%d').date()
        except ValueError as err:
            self.fail(err)

        delta = datetime.now().date() - generatedon
        self.assertTrue(
            delta.days < 120,  # pylint disable=E1103
            "eng/client_error.py is more than 120 days old ({0})".format(
                delta.days))  # pylint disable=E1103
