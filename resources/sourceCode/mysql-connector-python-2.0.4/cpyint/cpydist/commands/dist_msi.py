# MySQL Connector/Python - MySQL driver written in Python.
# Copyright (c) 2012, 2015, Oracle and/or its affiliates. All rights reserved.

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

"""Implements the Distutils command 'bdist_com_msi'

Implements the Distutils command 'bdist_com_msi' which creates a built
commercial distribution Windows Installer using Windows Installer XML 3.5.
The WiX file is available in the folder '/support/MSWindows/' of the
Connector/Python source.
"""

import os
import json
import re
from distutils import log
from distutils.errors import DistutilsError, DistutilsOptionError
from distutils.dir_util import remove_tree, copy_tree
from distutils.sysconfig import get_python_version
from distutils.core import Command

from ..utils import get_magic_tag, add_docs
from .. import wix
from . import COMMON_USER_OPTIONS, EDITION, VERSION, ARCH_64BIT

COMMERCIAL_DATA = os.path.abspath(os.path.join('cpyint', 'data', 'commercial'))
WIX_INSTALL = r"C:\Program Files (x86)\Windows Installer XML v3.5"
MSIDATA_ROOT = os.path.join('cpyint', 'data', 'MSWindows')

if VERSION >= (2, 1):
    CEXT_OPTIONS = [
        ('with-mysql-capi=', None,
         "Location of MySQL C API installation (Connector/C or MySQL Server)")
    ]
else:
    CEXT_OPTIONS = []


class _MSIDist(Command):

    """"Create a MSI distribution"""

    user_options = [
        ('bdist-dir=', 'd',
         "temporary directory for creating the distribution"),
        ('keep-temp', 'k',
         "keep the pseudo-installation tree around after " +
         "creating the distribution archive"),
        ('dist-dir=', 'd',
         "directory to put final built distributions in"),
        ('wix-install', None,
         "location of the Windows Installer XML installation"
         "(default: %s)" % WIX_INSTALL),
        ('python-version=', None,
         "target Python version"),
    ] + COMMON_USER_OPTIONS + CEXT_OPTIONS

    boolean_options = [
        'keep-temp', 'include-sources'
    ]

    negative_opt = {}

    def initialize_options(self):
        self.prefix = None
        self.build_base = None
        self.with_mysql_capi = None
        self.bdist_dir = None
        self.keep_temp = 0
        self.dist_dir = None
        self.include_sources = True
        self.wix_install = WIX_INSTALL
        self.python_version = get_python_version()[:3]
        self.edition = EDITION
        self.with_mysql_capi = None

    def finalize_options(self):
        self.set_undefined_options('build',
                                   ('build_base', 'build_base'))
        self.set_undefined_options('bdist',
                                   ('dist_dir', 'dist_dir'))

        if not self.prefix:
            self.prefix = os.path.join(self.build_base, 'wininst')

        supported = ['2.6', '2.7', '3.3', '3.4']
        if self.python_version not in supported:
            raise DistutilsOptionError(
                "The --python-version should be a supported version, one "
                "of %s" % ','.join(supported))

        if self.python_version[0] != get_python_version()[0]:
            raise DistutilsError(
                "Python v3 distributions need to be build with a "
                "supported Python v3 installation.")

        if self.with_mysql_capi:
            cmd_build = self.get_finalized_command('build')
            self.connc_lib = os.path.join(cmd_build.build_temp, 'connc', 'lib')
            self.connc_include = os.path.join(cmd_build.build_temp,
                                              'connc', 'include')

            self._finalize_connector_c(self.with_mysql_capi)
        else:
            self.connc_lib = None
            self.connc_lib = None

    def _finalize_connector_c(self, connc_loc):
        if not os.path.isdir(connc_loc):
            log.error("MySQL C API should be a directory")
            sys.exit(1)

        copy_tree(os.path.join(connc_loc, 'lib'), self.connc_lib)
        copy_tree(os.path.join(connc_loc, 'include'), self.connc_include)

        for lib_file in os.listdir(self.connc_lib):
            if os.name == 'posix' and not lib_file.endswith('.a'):
                os.unlink(os.path.join(self.connc_lib, lib_file))

    def _get_wixobj_name(self, myc_version=None, python_version=None):
        """Get the name for the wixobj-file

        Returns a string
        """
        raise NotImplemented

    def _create_msi(self, dry_run=0):
        """Create the Windows Installer using WiX
        
        Creates the Windows Installer using WiX and returns the name of
        the created MSI file.
        
        Raises DistutilsError on errors.
        
        Returns a string
        """
        # load the upgrade codes
        with open(os.path.join(MSIDATA_ROOT, 'upgrade_codes.json')) as fp:
            upgrade_codes = json.load(fp)

        # version variables for Connector/Python and Python
        mycver = self.distribution.metadata.version
        match = re.match("(\d+)\.(\d+).(\d+).*", mycver)
        if not match:
            raise ValueError("Failed parsing version from %s" % mycver)
        (major, minor, patch) = match.groups()
        pyver = self.python_version
        pymajor = pyver[0]
        
        # check whether we have an upgrade code
        try:
            upgrade_code = upgrade_codes[mycver[0:3]][pyver]
        except KeyError:
            raise DistutilsError(
                "No upgrade code found for version v{cpy_ver}, "
                "Python v{py_ver}".format(
                    cpy_ver=mycver, py_ver=pyver
                ))
        log.info("upgrade code for v%s, Python v%s: %s" % (
                 mycver, pyver, upgrade_code))
        
        # wixobj's basename is the name of the installer
        wixobj = self._get_wixobj_name()
        msi = os.path.abspath(
            os.path.join(self.dist_dir, wixobj.replace('.wixobj', '.msi')))
        wixer = wix.WiX(self.wxs,
                        out=wixobj,
                        msi_out=msi,
                        base_path=self.build_base,
                        install=self.wix_install)

        # correct newlines and version in text files
        log.info("Fixing newlines in text files")
        info_files = []
        for txt_file_dest, txt_file_path in self.fix_txtfiles.items():
            txt_fixed = os.path.join(self.build_base, txt_file_dest)
            info_files.append(txt_fixed)
            content = open(txt_file_path, 'rb').read()

            if b'\r\n' not in content:
                log.info("converting newlines in %s", txt_fixed)
                content = content.replace(b'\n', b'\r\n')
                open(txt_fixed, 'wb').write(content)
            else:
                log.info("not converting newlines in %s, this is odd",
                         txt_fixed)

        digit_needle = 'Connector/Python \d{1,2}.\d{1,2}'
        xy_needle = 'Connector/Python X.Y'
        xy_sub = 'Connector/Python {0}.{1}'
        for info_file in info_files:
            log.info("correcting version in %s", info_file)
            with open(info_file, 'r+') as fp:
                content = fp.readlines()
                for i, line in enumerate(content):
                    content[i] = re.sub(digit_needle,
                                        xy_sub.format(*VERSION[0:2]),
                                        line)
                    line = content[i]
                    content[i] = re.sub(xy_needle,
                                        xy_sub.format(*VERSION[0:2]),
                                        line)
                fp.seek(0)
                fp.write(''.join(content))

        # WiX preprocessor variables
        params = {
            'Version': '.'.join([major, minor, patch]),
            'FullVersion': mycver,
            'PythonVersion': pyver,
            'PythonMajor': pymajor,
            'Major_Version': major,
            'Minor_Version': minor,
            'Patch_Version': patch,
            'PythonInstallDir': 'Python%s' % pyver.replace('.', ''),
            'BDist': os.path.join(
                os.path.abspath(self.prefix), 'Lib', 'site-packages'),
            'PyExt': 'pyc' if not self.include_sources else 'py',
            'UpgradeCode': upgrade_code,
            'ManualPDF': os.path.abspath(
                os.path.join('docs', 'mysql-connector-python.pdf')),
            'ManualHTML': os.path.abspath(
                os.path.join('docs', 'mysql-connector-python.html')),
            'UpgradeCode': upgrade_code,
            'MagicTag': get_magic_tag(),
            'BuildDir': os.path.abspath(self.build_base),
            'HaveCExt': 1 if self.with_mysql_capi else 0,
            'LibMySQLDLL': os.path.join(
                os.path.abspath(self.connc_lib), 'libmysql.dll') \
                    if self.connc_lib else '',
        }
        
        wixer.set_parameters(params)
        
        if not dry_run:
            try:
                wixer.compile()
                wixer.link()
            except DistutilsError:
                raise

        if not self.keep_temp and not dry_run:
            log.info('WiX: cleaning up')
            os.unlink(msi.replace('.msi', '.wixpdb'))
        
        return msi

    def _prepare(self):
        log.info("Preparing installation in %s", self.build_base)
        cmd_install = self.reinitialize_command('install', reinit_subcommands=1)
        cmd_install.prefix = self.prefix
        cmd_install.with_mysql_capi = self.with_mysql_capi
        cmd_install.static = False
        cmd_install.ensure_finalized()
        cmd_install.run()

    def run(self):
        """Run the distutils command"""

        if os.name != 'nt':
            log.info("This command is only useful on Windows. "
                     "Forcing dry run.")
            self.dry_run = True

        self._prepare()

        wix.check_wix_install(wix_install_path=self.wix_install,
                              dry_run=self.dry_run)
        
        # create the Windows Installer
        msi_file = self._create_msi(dry_run=self.dry_run)
        log.info("created MSI as %s" % msi_file)
        
        if not self.keep_temp:
            remove_tree(self.build_base, dry_run=self.dry_run)


class BuiltCommercialMSI(_MSIDist):

    """Create a Built Commercial MSI distribution"""

    description = 'create a commercial built MSI distribution'
    user_options = [
        ('include-sources', None,
         "exclude sources built distribution (default: True)"),
    ] + _MSIDist.user_options

    boolean_options = _MSIDist.boolean_options + ['include-sources']
    
    def initialize_options (self):
        """Initialize the options"""
        _MSIDist.initialize_options(self)
        self.include_sources = None
    
    def finalize_options(self):
        """Finalize the options"""
        _MSIDist.finalize_options(self)

        self.wxs = os.path.join(MSIDATA_ROOT, 'product_com.wxs')

        self.fix_txtfiles = {
            'README.txt': os.path.join(COMMERCIAL_DATA, 'README_COM.txt'),
            'LICENSE.txt': os.path.join(COMMERCIAL_DATA, 'LICENSE_COM.txt'),
            'CHANGES.txt': os.path.join(os.getcwd(), 'CHANGES.txt'),
            'README_DOCS.txt': os.path.join(os.getcwd(), 'docs',
                                            'README_DOCS.txt'),
        }

    def _get_wixobj_name(self, myc_version=None, python_version=None):
        """Get the name for the wixobj-file

        Return string
        """
        mycver = myc_version or self.distribution.metadata.version
        pyver = python_version or self.python_version
        cext = '-cext' if self.with_mysql_capi else ''

        name_fmt = "mysql-connector-python-commercial-" \
                   "{conver}{cext}{edition}-py{pyver}"

        if VERSION < (2, 1):
            name_fmt += ".wixobj"
        else:
            name_fmt += "-{arch}.wixobj"

        return name_fmt.format(
                    conver=mycver,
                    cext=cext,
                    pyver=pyver,
                    edition=self.edition,
                    arch='winx64' if ARCH_64BIT else 'win32'
                )

    def _prepare(self):
        """Prepare the distribution"""
        log.info("Preparing installation in %s", self.build_base)
        cmd_install = self.reinitialize_command('install', reinit_subcommands=1)
        cmd_install.prefix = self.prefix
        cmd_install.with_mysql_capi = self.with_mysql_capi
        cmd_install.byte_code_only = 1
        cmd_install.commercial = 1
        cmd_install.static = False
        cmd_install.ensure_finalized()
        cmd_install.run()

        # documentation files should be available, even when empty
        add_docs('docs')


class GPLMSI(_MSIDist):

    """Create a GPL MSI distribution"""

    description = 'create a GPL MSI distribution'

    def finalize_options(self):
        """Finalize the options"""
        _MSIDist.finalize_options(self)

        self.wxs = os.path.join(MSIDATA_ROOT, 'product.wxs')
        self.fix_txtfiles = {
            'README.txt': os.path.join(os.getcwd(), 'README.txt'),
            'LICENSE.txt': os.path.join(os.getcwd(), 'LICENSE.txt'),
            'CHANGES.txt': os.path.join(os.getcwd(), 'CHANGES.txt'),
            'README_DOCS.txt': os.path.join(os.getcwd(), 'docs',
                                            'README_DOCS.txt'),
        }

    def _get_wixobj_name(self, myc_version=None, python_version=None):
        """Get the name for the wixobj-file

        Return string
        """
        mycver = myc_version or self.distribution.metadata.version
        pyver = python_version or self.python_version
        cext = '-cext' if self.with_mysql_capi else ''
        name_fmt = "mysql-connector-python-{conver}{cext}{edition}-py{pyver}"
        if VERSION < (2, 1):
            name_fmt += ".wixobj"
        else:
            name_fmt += "-{arch}.wixobj"
        return name_fmt.format(
                    conver=mycver,
                    cext=cext,
                    pyver=pyver,
                    edition=self.edition,
                    arch='winx64' if ARCH_64BIT else 'win32'
                )

