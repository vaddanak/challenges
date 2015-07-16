# MySQL Connector/Python - MySQL driver written in Python.
# Copyright (c) 2014, Oracle and/or its affiliates. All rights reserved.

%define name_gpl	mysql-connector-python
%define name_gpl_py3	mysql-connector-python3

%if 0%{?rhel} && 0%{?rhel} <= 5
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%if 0%{?fedora} > 12
%global with_python3 1
%endif

# SuSE
%if %(test -f /etc/SuSE-release && echo 1 || echo 0)
%define susever %(rpm -qf --qf '%%{version}\\n' /etc/SuSE-release | cut -d. -f1)
%define dist   .sles%{susever}
%endif

Summary:       Standardized MySQL driver for Python
Name:          mysql-connector-python-commercial
Version:       %{version}
Release:       1%{?dist}
License:       Commercial
Group:         Development/Libraries
URL:           https://www.mysql.com
Source0:       mysql-connector-python-commercial-%{version}.tar.gz
BuildArch:     noarch
Requires:      python
BuildRequires: python-devel
Conflicts:     %{name_gpl}
Obsoletes:     %{name} <= %{version}, %{name_gpl} <= %{version}
%if 0%{?with_python3}
BuildRequires: python3-devel
Conflicts:     %{name_gpl_py3}
Obsoletes:     %{name} <= %{version}, %{name_gpl_py3} <= %{version}
%endif # if with_python3
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
MySQL Connector/Python enables Python programs to access MySQL
databases, using an API that is compliant with the Python DB API
version 2.0. It is written in pure Python.

This is a release of MySQL Connector/Python, Oracle's dual-
license Python Driver for MySQL. For the avoidance of
doubt, this particular copy of the software is released
under a commercial license and the GNU General Public
License does not apply. MySQL Connector/Python is brought
to you by Oracle.

%if 0%{?with_python3}
%package -n    mysql-connector-python3-commercial
Requires:      python3
Summary:       Standardized MySQL driver for Python 3
Group:         Development/Libraries

%description -n mysql-connector-python3-commercial
MySQL Connector/Python enables Python programs to access MySQL
databases, using an API that is compliant with the Python DB API
version 2.0. It is written in pure Python.

This is the Python 3 version of the driver.

This is a release of MySQL Connector/Python, Oracle's dual-
license Python Driver for MySQL. For the avoidance of
doubt, this particular copy of the software is released
under a commercial license and the GNU General Public
License does not apply. MySQL Connector/Python is brought
to you by Oracle.
%endif # if with_python3

%prep
%setup -q
%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # if with_python3

%build
%{__python} setup.py build
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif # with_python3

%install
rm -rf %{buildroot}
%{__python} setup.py install --root %{buildroot}
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --root %{buildroot}
popd
%endif # with_python3

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc LICENSE.txt CHANGES.txt README.txt docs/README_DOCS.txt
%if ! 0%{?suse_version}
%{python_sitelib}/mysql
%endif
%if 0%{?rhel} > 5 || 0%{?fedora} > 12
%{python_sitelib}/mysql_connector_python*egg-info
%endif
%if 0%{?suse_version} && 0%{?suse_version} >= 1100
/usr/local/%_lib/python%py_ver/site-packages/mysql
/usr/local/%_lib/python%py_ver/site-packages/mysql_connector_python*.egg-info
%endif

%if 0%{?with_python3}
%files -n mysql-connector-python3-commercial
%defattr(-, root, root, -)
%doc LICENSE.txt CHANGES.txt README.txt docs/README_DOCS.txt
%{python3_sitelib}/mysql
%{python3_sitelib}/mysql_connector_python*egg-info
%endif # with_python3

%changelog
* Wed Mar 25 2015  Geert Vanderkelen <geert.vanderkelen@oracle.com> - 2.1.2-1
- Fix SuSE build

* Mon Oct 20 2014  Geert Vanderkelen <geert.vanderkelen@oracle.com> - 2.1.1-1
- Initial version for 2.1.1
