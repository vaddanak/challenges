# MySQL Connector/Python - MySQL driver written in Python.
# Copyright (c) 2012, 2015, Oracle and/or its affiliates. All rights reserved.

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

%define mysql_license   GPLv2
%define python_version  %(python -c "import distutils.sysconfig as ds; print ds.get_version()")
%define name        %(python -c "import setupinfo as m; print m.name.lower().replace('_','-')")
%define name_com    %(python -c "import setupinfo as m; print '%s-commercial' % m.name.lower().replace('_','-')")
%define version     %(python -c "import setupinfo as m; print m.version")
%define summary     %(python -c "import setupinfo as m; print m.description")
%define vendor      %(python -c "import setupinfo as m; print m.author")
%define packager    Oracle and/or its affiliates Product Engineering Team <mysql-build@oss.oracle.com>

# $ rpm --showrc | grep -e _build_name_fmt -e _rpmfilename
%define _rpmfilename %%{ARCH}/%%{NAME}-%%{VERSION}%{?edition}-%%{RELEASE}.%%{ARCH}.rpm

# SuSE
%if %(test -f /etc/SuSE-release && echo 1 || echo 0)
%define susever %(rpm -qf --qf '%%{version}\\n' /etc/SuSE-release | cut -d. -f1)
%define dist   .sles%{susever}
%endif

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib())")}

Name:       %{name}
Version:    %{version}
Release:    1%{?dist}
Summary:    %{summary}

Group:      Development/Libraries
License:    Copyright (c) 2009, 2014, Oracle and/or its affiliates. All rights reserved.  Use is subject to license terms.  Under %{mysql_license} license as shown in the Description field.
Vendor:     %{vendor}
Packager:   %{packager}
URL:        http://dev.mysql.com/downloads/connector/python/
Source0:    %{name}-%{version}%{?edition}.tar.gz
BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:  noarch

BuildRequires:  python
Requires:   python
Conflicts:  %{name_com}
Provides:   %{name} = %{version}
Obsoletes:  %{name} <= %{version}, %{name_com} <= %{version}

%description
MySQL Connector/Python enables Python programs to access MySQL
databases, using an API that is compliant with the Python DB API
version 2.0. It is written in pure Python and does not have any
dependencies except for the Python Standard Library.

%prep
%setup -n %{name}-%{version}%{?edition}

%install
%{__python} setup.py install -O1 --root=$RPM_BUILD_ROOT --prefix=%{_prefix} \
    --record=INSTALLED_FILES

# Removing the shared __init__.py[c] file(s), recreated in %post
TMP=`grep 'mysql/__init__.py' INSTALLED_FILES | head -n1`
PKGLOC=`dirname $TMP`
sed -i '/mysql\/__init__.py/d' INSTALLED_FILES
rm $RPM_BUILD_ROOT$PKGLOC/__init__.py* 2>/dev/null 1>&2

%clean
rm -rf ${buildroot}

%files -f INSTALLED_FILES
%defattr(-,root,root,-)
%doc LICENSE.txt CHANGES.txt README.txt docs/README_DOCS.txt

%post
touch %{python_sitelib}/mysql/__init__.py

%postun
if [ $1 == 0 ];
then
    # Non empty directories will be left alone
    rmdir %{python_sitelib}/mysql/connector/locales/eng 2>/dev/null
    rmdir %{python_sitelib}/mysql/connector/locales 2>/dev/null
    rmdir %{python_sitelib}/mysql/connector/django 2>/dev/null
    rmdir %{python_sitelib}/mysql/connector/fabric 2>/dev/null
    rmdir %{python_sitelib}/mysql/connector 2>/dev/null

    # Try to remove the MySQL top package mysql/
    SUBPKGS=`ls --ignore=*.py{c,o} -m %{python_sitelib}/mysql`
    if [ "$SUBPKGS" == "__init__.py" ];
    then
        rm %{python_sitelib}/mysql/__init__.py* 2>/dev/null 1>&2
        # This should not fail, but show error if any
        rmdir %{python_sitelib}/mysql/
    fi
    exit 0
fi


%changelog
* Thu Apr  9 2014 Geert Vanderkelen <geert.vanderkelen@oracle.com> - 2.0.0

- README was renamed as README.txt
- COPYING was renamed as LICENSE.txt

* Fri Mar 28 2014 Geert Vanderkelen <geert.vanderkelen@oracle.com> - 2.0.0

- Changing metasetupinfo.py to setupinfo.py.
- Fixing 'bogus' log entries.

* Fri Mar  7 2014 Peeyush Gupta <peeyush.x.gupta@oracle.com> - 1.2.1

- Added removal of the fabric folder.

* Mon Nov  4 2013 Geert Vanderkelen <geert.vanderkelen@oracle.com> - 1.1.4

- Is not possible to 'upgrade' the GPL edition to Commercial Edition.
- Added removal of the django folder.

* Fri Sep 20 2013 Geert Vanderkelen <geert.vanderkelen@oracle.com> - 1.1.2

- It is now possible to set the 'edition' variable for special releases

* Mon Mar  4 2013 Geert Vanderkelen <geert.vanderkelen@oracle.com> - 1.0.10

- Remove documentation files, repladed by README_DOCS.txt.

* Mon Feb 18 2013 Geert Vanderkelen <geert.vanderkelen@oracle.com> - 1.0.9

- 'prep' is now used to unpack the source distribution
- 'install' now use the setup.py script
- 'files' using the INSTALLED_FILES and installs documentation
- 'post' now creates the mysql/__init__.py which does not get
  installed any longer since shared by multiple projects
- 'postun' cleans up the directories and tries to remove the
  top package mysql/
- Updating the copyright.

* Thu Aug 16 2012 Geert Vanderkelen <geert.vanderkelen@oracle.com>

- Name of the commercial package includes 'commercial'
- Removed 'Source' and replaced 'URL' with Connector/Python download URL
- Added the Packager information
- Adding documentation files

* Tue Jul 31 2012 Kent Boortz <kent.boortz@oracle.com>

- Aligned commercial and GPL spec files
- Use "python" in PATH, to be able to specify a recent enough Python
- Set sitedir, "{_rpmconfigdir}/macros.python" is missing in some distros

* Tue Jun 05 2012 Geert Vanderkelen <geert.vanderkelen@oracle.com> - 1.0.3

- Initial implementation.
