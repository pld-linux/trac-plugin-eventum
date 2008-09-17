Summary:	Plugin for linking Eventum issues in Trac
Name:		trac-plugin-eventum
Version:	0.2
Release:	1
License:	BSD-like
Group:		Applications/WWW
BuildRequires:	cvs
BuildRequires:	python-devel
BuildRequires:	python-setuptools
BuildRequires:	rpmbuild(macros) >= 1.268
%pyrequires_eq  python-modules
Requires:	trac >= 0.10
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_cvsroot	:ext:cvs.delfi.ee:/usr/local/cvs
%define		_cvsmodule	trac/plugins/eventum

%description
Plugin for linking Eventum issues in Trac

%prep
%setup -qcT
cd ..
cvs -d %{_cvsroot} co %{?_cvstag:-r %{_cvstag}} -d %{name}-%{version} -P %{_cvsmodule}
cd -

%build
# skip tagging if we checkouted from tag or have debug enabled
# also make make tag only if we have integer release
%if %{!?debug:1}%{?debug:0} && %{!?_cvstag:1}%{?_cvstag:0} && %([[ %{release} = *.* ]] && echo 0 || echo 1)
# do tagging by version
tag=%{name}-%(echo %{version} | tr . _)-%(echo %{release} | tr . _)

cd %{_specdir}
if [ $(cvs status -v %{name}.spec | egrep -c "$tag[[:space:]]") != 0 ]; then
	: "Tag $tag already exists"
	exit 1
fi
cvs tag $tag %{name}.spec
cd -
cvs tag $tag
%endif

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
	Don't forget to enable eventum in conf/trac.ini:

	[components]
	trac.eventum.* = enabled

	And restart Trac server.
EOF
#' - vim
fi

%files
%defattr(644,root,root,755)
%{py_sitescriptdir}/trac/eventum
%{py_sitescriptdir}/TracEventumLink-*.egg-info
