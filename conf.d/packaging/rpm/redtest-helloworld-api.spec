#
# spec file for package redtunamagic-ship
#

Name:           redtest-helloworld-api
Version:        1.0
Release:        1%{?dist}
Summary:        API that can be used as an example of how implement Redtests

License:        Apache-2.0
Group:          Development/Tools/Other
Vendor:         Armand Bénéteau <armand.beneteau@iot.bzh>
Url:            http://git.ovh.iot/redpesk/redtest-helloword-api
Source:         %{name}-%{version}.tar.bz2

BuildRequires:  python3
BuildRequires:  python3-rpm-macros
BuildRequires:  python3-setuptools
BuildRequires:  systemd

Requires:	python3-aiohttp

BuildArch:      noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Python API project that can be used as an example on how to implement Redtests in a project

%prep
%setup -q

%build
python3 setup.py build

%install
python3 setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
mkdir -p %{buildroot}%{_unitdir}/
cp conf.d/systemd/redtesthelloapi.service %{buildroot}%{_unitdir}/

%post
%systemd_post redtesthelloapi.service

%preun
%systemd_preun redtesthelloapi.service

%postun
%systemd_postun_with_restart redtesthelloapi.service

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%license LICENSE
%doc README.md
%{_bindir}/redtesthelloworldd
%{_unitdir}/redtesthelloapi.service
%{python3_sitelib}/redtest_helloworld_api
%{python3_sitelib}/redtest_helloworld_api-*.egg-info

%changelog
