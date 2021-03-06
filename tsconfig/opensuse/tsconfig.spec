Summary: StarlingX Config Info
Name: tsconfig
Version: 1.0.0
Release: %{tis_patch_ver}%{?_tis_dist}
License: Apache-2.0
Group: Development/Languages/Python
URL: https://opendev.org/starlingx/update
Source0: %{name}-%{version}.tar.gz

%define debug_package %{nil}

BuildRequires: python-setuptools
BuildRequires: python2-pip

%description
StarlingX Project Config Info

%define local_dir /usr/
%define local_bindir %{local_dir}/bin/
%define pythonroot /usr/lib64/python2.7/site-packages

%prep
%setup -n %{name}-%{version}/%{name}

%build
%{__python} setup.py build

%install
%{__python} setup.py install --root=$RPM_BUILD_ROOT \
                             --install-lib=%{pythonroot} \
                             --prefix=/usr \
                             --install-data=/usr/share \
                             --single-version-externally-managed

install -d -m 755 %{buildroot}%{local_bindir}
install -p -D -m 700 scripts/tsconfig %{buildroot}%{local_bindir}/tsconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc LICENSE
%{local_bindir}/*
%dir %{pythonroot}/%{name}
%{pythonroot}/%{name}/*
%dir %{pythonroot}/%{name}-%{version}-py2.7.egg-info
%{pythonroot}/%{name}-%{version}-py2.7.egg-info/*

%changelog
