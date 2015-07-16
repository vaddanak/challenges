%if 0%{?rhel} && 0%{?rhel} <= 5
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%if 0%{?suse_version} && 0%{?suse_version} <= 1200
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

%if 0%{?fedora} > 12 
%global with_python3 1
%endif

Summary:       Standardized MySQL database driver for Python
Name:          mysql-connector-python
Version:       2.0.4
Release:       1%{?dist}
License:       GPLv2
Group:         Development/Libraries
URL:           https://dev.mysql.com/downloads/connector/python/            
Source0:       https://cdn.mysql.com/Downloads/Connector-Python/mysql-connector-python-%{version}.tar.gz
BuildArch:     noarch
BuildRequires: python-devel
%if 0%{?with_python3}
BuildRequires: python3-devel
%endif # if with_python3
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%description
MySQL Connector/Python enables Python programs to access MySQL
databases, using an API that is compliant with the Python DB API
version 2.0. It is written in pure Python and does not have any
dependencies except for the Python Standard Library.

%if 0%{?with_python3}
%package -n    mysql-connector-python3
Summary:       Standardized MySQL database driver for Python 3
Group:         Development/Libraries

%description -n mysql-connector-python3
MySQL Connector/Python enables Python programs to access MySQL
databases, using an API that is compliant with the Python DB API
version 2.0. It is written in pure Python and does not have any
dependencies except for the Python Standard Library.

This is the Python 3 version of the driver.
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
%{__python} setup.py install --prefix=%{_prefix} --skip-build --root %{buildroot}
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --prefix=%{_prefix} --skip-build --root %{buildroot}
popd
%endif # with_python3

%clean
rm -rf %{buildroot}

%check
%{__python} unittests.py --mysql-basedir=%{_prefix} || :
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} unittests.py --mysql-basedir=%{_prefix} || :
popd
%endif # with_python3

%files
%defattr(-, root, root, -)
%doc LICENSE.txt CHANGES.txt README.txt docs/README_DOCS.txt
%{python_sitelib}/mysql
%if 0%{?rhel} > 5 || 0%{?fedora} > 12
%{python_sitelib}/mysql_connector_python-*.egg-info
%endif
%if 0%{?suse_version} && 0%{?suse_version} >= 1100
%{python_sitelib}/mysql_connector_python*.egg-info
%endif


%if 0%{?with_python3}
%files -n mysql-connector-python3
%defattr(-, root, root, -)
%doc LICENSE.txt CHANGES.txt README.txt docs/README_DOCS.txt
%{python3_sitelib}/mysql
%{python3_sitelib}/mysql_connector_python-*.egg-info
%endif # with_python3

%changelog
* Tue Mar 31 2015  Peeyush Gupta <peeyush.x.gupta@oracle.com> - 2.0.4-1
- Update for 2.0.4

* Thu Dec 18 2014  Geert Vanderkelen <geert.vanderkelen@oracle.com> - 2.0.3-1
- Updated for 2.0.3
- Fixed the build prefix for sles 

* Mon Oct 14 2014  Geert Vanderkelen <geert.vanderkelen@oracle.com> - 2.0.2-1
- Updated for 2.0.2

* Mon Sep 01 2014  Balasubramanian Kandasamy <balasubramanian.kandasamy@oracle.com> - 2.0.1-1
- Updated for 2.0.1

* Wed Jul 30 2014  Balasubramanian Kandasamy <balasubramanian.kandasamy@oracle.com> - 1.2.3-1
- Updated for 1.2.3

* Tue May 13 2014  Balasubramanian Kandasamy <balasubramanian.kandasamy@oracle.com> - 1.2.2-1
- Updated for 1.2.2

* Tue Apr 01 2014  Balasubramanian Kandasamy <balasubramanian.kandasamy@oracle.com> - 1.1.7-1
- Updated for 1.1.7

* Wed Feb 12 2014  Balasubramanian Kandasamy <balasubramanian.kandasamy@oracle.com> - 1.1.6-1
- Updated for 1.1.6

* Wed Jan 22 2014  Balasubramanian Kandasamy <balasubramanian.kandasamy@oracle.com> - 1.1.5-1
- Updated for 1.1.5

* Fri Dec 06 2013  Balasubramanian Kandasamy <balasubramanian.kandasamy@oracle.com> - 1.1.4-1
- initial package
