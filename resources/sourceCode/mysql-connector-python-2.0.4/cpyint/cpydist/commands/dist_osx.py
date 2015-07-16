# MySQL Connector/Python - MySQL driver written in Python.
# Copyright (c) 2013, 2015, Oracle and/or its affiliates. All rights reserved.

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

"""Implements the Distutils commands making packages for OS X"""

import os
import platform
import re
import string
import sys

from distutils import log
from distutils.command.bdist import bdist
from distutils.file_util import copy_file
from distutils.dir_util import copy_tree, remove_tree

from . import VERSION, CEXT_OPTIONS

OSX_PKGS = {
    'pure': os.path.join('cpyint', 'data', 'OSX', 'pure'),
}
if VERSION >= (2, 1):
    OSX_PKGS.update({
        'cext': os.path.join('cpyint', 'data', 'OSX', 'cext'),
    })

COMMERCIAL_DATA = os.path.join('cpyint', 'data', 'commercial')


class BuildDistOSX(bdist):

    """Distutils Command building OS X package"""

    platf_n = '-osx'
    platf_v = '.'.join(platform.mac_ver()[0].split('.', 2)[0:2])
    description = 'create OSX GPL distribution package'
    user_options = [
        ('keep-temp', 'k',
         "keep the pseudo-installation tree around after "
         "creating the distribution archive"),
        ('debug', None,
         "turn debugging on"),
        ('create-dmg', 'c',
         "create a dmg image from the resulting package file "
         "(default 'False')"),
        ('sign', 's',
         "signs the package file (default 'False')"),
        ('identity=', 'i',
         "identity or name of the certificate to use to sign the package file"
         "(default 'MySQL Connector/Python')"),
        ('dist-dir=', 'd',
         "directory to put final built distributions in"),
        ('platform=', 'p',
         "name of the platform in resulting file "
         "(default '{0}')".format(platf_n)),
        ('platform-version=', 'v',
         "version of the platform in resulting file "
         "(default '{0}')".format(platf_v))
    ] + CEXT_OPTIONS

    boolean_options = ['keep-temp', 'create-dmg', 'sign']

    def initialize_options(self):
        """Initialize the options"""
        self.name = self.distribution.get_name()
        self.version = self.distribution.get_version()
        self.keep_temp = None
        self.create_dmg = False
        self.dist_dir = None
        self.started_dir = os.getcwd()
        self.platform = self.platf_n
        self.platform_version = self.platf_v
        self.debug = False
        self.osx_pkg_name = "{0}-{1}.pkg".format(self.name, self.version)
        self.dstroot = "dstroot"
        self.sign = False
        self.identity = "MySQL Connector/Python"
        self.with_mysql_capi = None

    def finalize_options(self):
        """Finalize the options"""
        self.set_undefined_options('bdist',
                                   ('dist_dir', 'dist_dir'))

    def _prepare_pgk_base(self, template_name, data_dir, root='', gpl=True):
        """Create and populate the src base directory
        """

        # copy and create necessary files
        osx_dist_name = template_name.format(self.name, self.version)
        osx_pkg_name = "{0}.pkg".format(osx_dist_name)
        osx_pkg_contents = os.path.join(root, osx_pkg_name, 'Contents')
        osx_pkg_resrc = os.path.join(osx_pkg_contents, 'Resources')
        self.mkpath(osx_pkg_resrc)
        osx_path = os.path.join(root, self.dstroot)

        cwd = os.path.join(os.getcwd())

        copy_file_src_dst = [
            (os.path.join(data_dir, "PkgInfo"),
             os.path.join(osx_pkg_contents, "PkgInfo")),
        ]

        readme_loc = os.path.join(osx_pkg_resrc, "ReadMe.txt")
        license_loc = os.path.join(osx_pkg_resrc, "License.txt")
        changes_loc = os.path.join(osx_pkg_resrc, "Changes.txt")

        # No special folder for GPL or commercial. Files inside the directory
        # will determine what it is.
        data_path = os.path.join(
            osx_path, 'usr', 'local',
            template_name.format(self.name, self.version)
        )
        self.mkpath(data_path)

        if gpl:
            data_path = os.path.join(
                osx_path, 'usr', 'local',
                template_name.format(self.name, self.version))
            copy_file_src_dst += [
                (os.path.join(cwd, "README.txt"), readme_loc),
                (os.path.join(cwd, "LICENSE.txt"), license_loc),
                (os.path.join(cwd, "CHANGES.txt"), changes_loc),
                (os.path.join(cwd, "README.txt"),
                 os.path.join(data_path, "ReadMe.txt")),
                (os.path.join(cwd, "LICENSE.txt"),
                 os.path.join(data_path, "License.txt")),
                (os.path.join(cwd, "CHANGES.txt"),
                 os.path.join(data_path, "Changes.txt")),
            ]
        else:
            copy_file_src_dst += [
                (os.path.join(COMMERCIAL_DATA, "README_COM.txt"), readme_loc),
                (os.path.join(COMMERCIAL_DATA, "LICENSE_COM.txt"), license_loc),
                (os.path.join(cwd, "CHANGES.txt"), changes_loc),
                (os.path.join(COMMERCIAL_DATA, "README_COM.txt"),
                 os.path.join(data_path, "ReadMe.txt")),
                (os.path.join(COMMERCIAL_DATA, "LICENSE_com.txt"),
                 os.path.join(data_path, "License.txt")),
                (os.path.join(cwd, "CHANGES.txt"),
                 os.path.join(data_path, "Changes.txt")),
            ]

        pkg_files = [
            (os.path.join(data_dir, "Info.plist"),
             os.path.join(osx_pkg_contents, "Info.plist")),
            (os.path.join(data_dir, "Description.plist"),
             os.path.join(osx_pkg_resrc, "Description.plist")),
            (os.path.join(data_dir, "Welcome.rtf"),
             os.path.join(osx_pkg_resrc, "Welcome.rtf")),
        ]

        major_version = self.version.split('.')[0]
        minor_version = self.version.split('.')[1]

        for pkg_file, dest_file in pkg_files:
            with open(pkg_file) as fp:
                template = string.Template(fp.read())

                content = template.substitute(
                    version=self.version,
                    major=major_version,
                    minor=minor_version
                )

                with open(dest_file, 'w') as fp_dest:
                    fp_dest.write(content)

        for src, dst in copy_file_src_dst:
            copy_file(src, dst)

        info_files = [
            license_loc,
            readme_loc,
            os.path.join(data_path, "ReadMe.txt"),
            os.path.join(data_path, "License.txt"),
        ]
        re_needle = 'Connector/Python \d{1,2}.\d{1,2}'
        xy_needle = 'Connector/Python X.Y'
        version_fmt = 'Connector/Python {0}.{1}'
        for info_file in info_files:
            log.info("correcting version in %s", info_file)
            with open(info_file, 'r+') as fp:
                content = fp.readlines()
                for i, line in enumerate(content):
                    content[i] = re.sub(re_needle,
                                        version_fmt.format(*VERSION[0:2]),
                                        line)
                    content[i] = line.replace(xy_needle,
                                              version_fmt.format(*VERSION[0:2]))

                fp.seek(0)
                fp.write(''.join(content))

    def _create_pkg(self, template_name, dmg=False, sign=False, root='',
                    identity=''):
        """Create the mac osx pkg and a dmg image if it is required
        """

        osx_dist_name = template_name.format(self.name, self.version)
        osx_pkg_name = "{0}.pkg".format(osx_dist_name)
        osx_pkg_contents = os.path.join(osx_pkg_name, 'Contents')

        os.chdir(root)
        log.info("Root directory: {0}".format(os.getcwd()))

        # create a bom(8) file to tell the installer which files need to be
        # installed
        log.info("creating Archive.bom file, that describe files to install")
        log.info("dstroot {0}".format(self.dstroot))
        archive_bom_path = os.path.join(osx_pkg_contents, 'Archive.bom')
        self.spawn(['mkbom', self.dstroot, archive_bom_path])

        # Create an archive of the files to install
        log.info("creating Archive.pax with files to be installed")
        os.chdir(self.dstroot)

        pax_file = '../{NAME}/Contents/Archive.pax'.format(NAME=osx_pkg_name)
        self.spawn(['pax', '-w', '-x', 'cpio', '.', '-f', pax_file])
        os.chdir('../')

        # Sign the package
        # In Order to be possible the certificates needs to be installed
        if sign:
            log.info("Signing the package")
            osx_pkg_name_signed = '{0}_s.pkg'.format(osx_dist_name)
            self.spawn(['productsign', '--sign', identity,
                        osx_pkg_name,
                        osx_pkg_name_signed])
            self.spawn(['spctl', '-a', '-v', '--type', 'install',
                        osx_pkg_name_signed])
            osx_pkg_name = osx_pkg_name_signed

        # Create a .dmg image
        if dmg:
            log.info("Creating dmg file")
            self.spawn(['hdiutil', 'create', '-volname', osx_dist_name,
                        '-srcfolder', osx_pkg_name, '-ov', '-format',
                        'UDZO', '{0}.dmg'.format(osx_dist_name)])

        log.info("Current directory: {0}".format(os.getcwd()))

        for base, dirs, files in os.walk(os.getcwd()):
            for filename in files:
                if filename.endswith('.dmg'):
                    new_name = filename.replace(
                        '{0}'.format(self.version),
                        '{0}{1}{2}'.format(self.version, self.platform,
                                                 self.platform_version)
                    )
                    file_path = os.path.join(base, filename)
                    file_dest = os.path.join(self.started_dir,
                                             self.dist_dir, new_name)
                    copy_file(file_path, file_dest)
                    break
            for dir_name in dirs:
                if dir_name.endswith('.pkg'):
                    new_name = dir_name.replace(
                        '{0}'.format(self.version),
                        '{0}{1}{2}'.format(self.version, self.platform,
                                                 self.platform_version)
                    )
                    dir_dest = os.path.join(self.started_dir,
                                            self.dist_dir, new_name)
                    copy_tree(dir_name, dir_dest)
                    break
            break

    def run(self):
        """Run the distutils command"""
        self.mkpath(self.dist_dir)

        self.debug = self.verbose

        cmd_build = self.get_finalized_command('build')
        build_base = os.path.abspath(cmd_build.build_base)
        metadata_name = self.distribution.metadata.name

        for key, data_dir in OSX_PKGS.items():
            osx_root = os.path.join(build_base, 'osx_' + key)

            cmd_install = self.reinitialize_command('install',
                                                    reinit_subcommands=1)
            cmd_install.compile = False
            if key == 'cext':
                cmd_install.distribution.metadata.name = metadata_name + '-cext'
                cmd_install.with_mysql_capi = self.with_mysql_capi
            else:
                cmd_install.distribution.metadata.name = metadata_name
                cmd_install.with_mysql_capi = None
                cmd_install.need_ext = False
            cmd_install.root = os.path.join(osx_root, self.dstroot)

            cmd_install.ensure_finalized()
            cmd_install.run()

            if key is not 'pure':
                template_name = "{0}-%s-{1}" % key
            else:
                template_name = "{0}-{1}"

            self._prepare_pgk_base(template_name, data_dir, root=osx_root)

            self._create_pkg(template_name, dmg=self.create_dmg, root=osx_root,
                             sign=self.sign, identity=self.identity)

            os.chdir(self.started_dir)

            # Ensure we are building again
            if os.path.isdir(cmd_install.build_lib):
                log.info("removing %s", cmd_install.build_lib)
                remove_tree(cmd_install.build_lib)

        if not self.keep_temp:
            remove_tree(build_base, dry_run=self.dry_run)


class BuildDistOSXcom(BuildDistOSX):

    """Distutils Command building commercial OS X package"""

    description = 'create OSX commercial distribution package'

    boolean_options = ['keep-temp', 'create-dmg', 'sign']

    def finalize_options(self):
        """Finalize the options"""
        self.set_undefined_options('bdist',
                                   ('dist_dir', 'dist_dir'))

    def run(self):
        """Run the distutils command"""
        self.mkpath(self.dist_dir)
        self.debug = self.verbose

        cmd_build = self.get_finalized_command('build')
        build_base = os.path.abspath(cmd_build.build_base)
        metadata_name = self.distribution.metadata.name

        if self.with_mysql_capi:
            dist_type = 'cext'
        else:
            dist_type = 'pure'
        data_dir = OSX_PKGS[dist_type]

        osx_root = os.path.join(build_base, 'osx_' + dist_type)

        cmd_install = self.reinitialize_command('install',
                                                reinit_subcommands=1)
        cmd_install.compile = True  # True! Important for Commercial
        cmd_install.commercial = True
        cmd_install.byte_code_only = 1
        if dist_type == 'cext':
            cmd_install.distribution.metadata.name = metadata_name + '-cext'
            cmd_install.with_mysql_capi = self.with_mysql_capi
        else:
            cmd_install.distribution.metadata.name = metadata_name
            cmd_install.with_mysql_capi = None
            cmd_install.need_ext = False
        cmd_install.root = os.path.join(osx_root, self.dstroot)

        cmd_install.ensure_finalized()
        cmd_install.run()

        if dist_type is not 'pure':
            template_name = "{0}-%s-commercial-{1}" % dist_type
        else:
            template_name = "{0}-commercial-{1}"

        self._prepare_pgk_base(template_name, data_dir, root=osx_root,
                               gpl=False)

        self._create_pkg(template_name, dmg=self.create_dmg, root=osx_root,
                         sign=self.sign, identity=self.identity)

        os.chdir(self.started_dir)

        if not self.keep_temp:
            remove_tree(build_base, dry_run=self.dry_run)

    def run_old(self):
        """Run the distutils command"""
        log.info("self.name = {0}".format(self.name))
        self.mkpath(self.dist_dir)

        self.debug = self.verbose

        build_path = 'build'
        root = os.path.join(build_path, 'osx')
        osx_path = os.path.join(root, self.dstroot)
        self.mkpath(osx_path)

        bdist = self.get_finalized_command('bdist_com')
        bdist.dist_dir = root
        bdist.prefix = osx_path
        log.info("install_cmd.prefix {0}".format(bdist.prefix))
        if not self.debug:
            bdist.verbose = 0
        bdist.compile = False
        bdist.keep_temp = True
        purelib_path = os.path.join(osx_path, 'Library', 'Python',
                                    sys.version[0:3], 'site-packages')
        log.info("py_version {0}".format(purelib_path))
        bdist.bdist_dir = purelib_path

        bdist.bin_install_dir = os.path.join(osx_path, 'bin')
        self.run_command('bdist_com')

        log.info("bdist_com cmd finish")

        if self.distribution.data_files:
            install_cmd = self.get_finalized_command('install_data')
            log.info("install_cmd.dist_dir {0}".format(root))
            install_cmd.install_dir = root
            log.info("install_cmd.root {0}".format(osx_path))
            install_cmd.root = osx_path
            log.info("install_cmd.prefix {0}".format(bdist.prefix))

            self.run_command('install_data')
            log.info("install_cmd cmd finish")

        template_name = "{0}-commercial-{1}"
        self._prepare_pgk_base(template_name, osx_path, root=root, gpl=False)

        self._create_pkg(template_name,
                         dmg=self.create_dmg, root=root,
                         sign=self.sign, identity=self.identity)

        os.chdir(self.started_dir)

        if not self.keep_temp:
            remove_tree(build_path, dry_run=self.dry_run)

