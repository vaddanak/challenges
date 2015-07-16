%if 0%{?rhel} && 0%{?rhel} <= 5
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(plat_specific=True))")}
%endif

%if 0%{?suse_version} && 0%{?suse_version} <= 1200
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(plat_specific=True))")}
%endif

%if 0%{?fedora} > 12
%global with_python3 1
%endif



Summary:       Standardized MySQL driver for Python with C Extension
Name:          mysql-connector-python-cext
Version:       %{version}
Release:       1%{?dist}
License:       GPLv2
Group:         Development/Libraries
URL:           https://dev.mysql.com/downloads/connector/python/
Source0:       https://cdn.mysql.com/Downloads/Connector-Python/mysql-connector-python-%{version}.tar.gz
Requires:      python
BuildRequires: python-devel
%if 0%{?with_python3}
BuildRequires: python3-devel
%endif # if with_python3
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
%description
MySQL Connector/Python enables Python programs to access MySQL
databases, using an API that is compliant with the Python DB API
version 2.0. It is written in pure Python with optional
C Extension using MySQL client libraries.

%if 0%{?with_python3}
%package -n    mysql-connector-python3-cext
Requires:      python3
Summary:       Standardized MySQL driver for Python 3 with C Extension
Group:         Development/Libraries

%description -n mysql-connector-python3-cext
MySQL Connector/Python enables Python programs to access MySQL
databases, using an API that is compliant with the Python DB API
version 2.0. It is written in pure Python with optional
C Extension using MySQL client libraries.

This is the Python 3 version of the driver.
%endif # if with_python3

%prep
%setup -q -n mysql-connector-python-%{version}
%if 0%{?with_python3}
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif # if with_python3

%build
# Only build the C Extension
%{__python} setup.py build_ext_static --with-mysql-capi=%{mysql_capi}
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py build_ext_static --with-mysql-capi=%{mysql_capi}
popd
%endif # with_python3

%install
rm -rf %{buildroot}
%{__python} setup.py install --with-mysql-capi=/usr/bin/mysql_config \
	--skip-build --root %{buildroot}
%if 0%{?with_python3}
pushd %{py3dir}
%{__python3} setup.py install --with-mysql-capi=/usr/bin/mysql_config \
	--skip-build --root %{buildroot}
popd
%endif # with_python3
# We need 'cext' in the EGG files
EGGFILES=`find %{buildroot} -name '*egg-info'`
for eggfile in $EGGFILES; do \
  cextegg=`echo $eggfile | sed -e s/_python/_python_cext/`; \
  mv $eggfile $cextegg; \
done

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root, -)
%doc LICENSE.txt CHANGES.txt README.txt docs/README_DOCS.txt
%if 0%{?rhel} > 5 || 0%{?fedora} > 12
%{python_sitearch}/_mysql_connector.so
%{python_sitearch}/mysql_connector_python_cext-*.egg-info
%endif
%if 0%{?suse_version} && 0%{?suse_version} >= 1100
/usr/local/%_lib/python%py_ver/site-packages/_mysql_connector.so
/usr/local/%_lib/python%py_ver/site-packages/mysql_connector_python_cext-*.egg-info
%endif

%if 0%{?with_python3}
%files -n mysql-connector-python3-cext
%defattr(-, root, root, -)
%doc LICENSE.txt CHANGES.txt README.txt docs/README_DOCS.txt
%{python3_sitearch}/_mysql_connector*.so
%{python3_sitearch}/mysql_connector_python_cext-*.egg-info
%endif # with_python3

%changelog
* Mon Oct 20 2014  Geert Vanderkelen <geert.vanderkelen@oracle.com> - 2.1.1-1
- Initial version for 2.1.1
