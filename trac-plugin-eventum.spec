%define     trac_ver    0.12
%define		plugin		eventum
Summary:	Plugin for linking Eventum issues in Trac
Name:		trac-plugin-%{plugin}
Version:	0.4
Release:	2
License:	BSD-like
Group:		Applications/WWW
Source0:	https://github.com/eventum/trac-plugin-eventum/tarball/%{name}-0_4-1/%{plugin}-%{version}.tgz
# Source0-md5:	5fa029232b261e1732ac707aa8878f18
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildRequires:	rpmbuild(macros) >= 1.268
%pyrequires_eq  python-modules
Requires:	trac >= %{trac_ver}
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Plugin for linking Eventum issues in Trac

%prep
%setup -qc
# for github urls:
mv *-%{plugin}-*/* .

%build
%{__python} setup.py build
%{__python} setup.py egg_info

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--single-version-externally-managed \
	--optimize 2 \
	--root=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ "$1" = "1" ]; then
	%banner -e %{name} <<-'EOF'
	To enable and configure Eventum plugin, configure in conf/trac.ini:

	[components]
	trac.eventum.* = enabled

	[eventum]
	url = http://eventum.example.org/view.php?id=%d

	And restart Trac server.
EOF
#' - vim
fi

%files
%defattr(644,root,root,755)
%{py_sitescriptdir}/trac/%{plugin}
%{py_sitescriptdir}/TracEventumLink-*.egg-info
