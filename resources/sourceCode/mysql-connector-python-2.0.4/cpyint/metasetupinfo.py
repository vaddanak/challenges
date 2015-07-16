# MySQL Connector/Python - MySQL driver written in Python.
# Copyright (c) 2014, Oracle and/or its affiliates. All rights reserved.


from distutils import util
from distutils.dir_util import copy_tree
import os
import sys


def byte_compile(py_files, optimize=0, force=0, prefix=None, base_dir=None,
                 verbose=1, dry_run=0, direct=None):
    """Byte-compile Python source files

    This function calls the original distutils.util.byte_compile function but
    additionally removes the Python source files.

    This function is only to be used with non GPLv2 sources.
    """
    util.orig_byte_compile(py_files, optimize, force, prefix, base_dir,
                      verbose, dry_run, direct)

    for py_file in py_files:
        if 'mysql/__init__.py' in py_file:
            continue
        os.unlink(py_file)


try:
    from .cpydist.commands import (
        sdist, bdist, dist_rpm, dist_deb, dist_osx
    )

    from distutils import dir_util
    dir_util.copy_tree = copy_tree

    command_classes = {
        'sdist': sdist.GenericSourceGPL,
        'sdist_gpl': sdist.SourceGPL,
        'bdist_com': bdist.BuiltCommercial,
        'bdist_com_rpm': dist_rpm.BuiltCommercialRPM,
        'sdist_gpl_rpm': dist_rpm.SDistGPLRPM,
        'sdist_com': sdist.SourceCommercial,
        'sdist_gpl_deb': dist_deb.DebianBuiltDist,
        'bdist_com_deb': dist_deb.DebianCommercialBuilt,
        'sdist_gpl_osx': dist_osx.BuildDistOSX,
        'bdist_com_osx': dist_osx.BuildDistOSXcom,
    }

    try:
        from .cpydist.commands import install
        command_classes.update({
            'install': install.InstallInternal,
            'install_lib': install.InstallLibInternal,
        })
    except ImportError:
        # Works for Connector/Python 2.1 and later
        pass

    if sys.version_info >= (2, 7):
        # MSI only supported for Python 2.7 and greater
        from .cpydist.commands import (dist_msi)
        command_classes.update({
            'bdist_com': bdist.BuiltCommercial,
            'bdist_com_msi': dist_msi.BuiltCommercialMSI,
            'sdist_gpl_msi': dist_msi.GPLMSI,
        })

except ImportError:
    # Part of Source Distribution
    command_classes = {}
    raise
