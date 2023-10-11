#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests

Summary:	Python API and shell utilities to monitor file system events
Summary(pl.UTF-8):	API pythonowe i narzędzia powłoki do monitorowania zdarzeń systemu plików
Name:		python-watchdog
# keep 0.x here for python3 support
Version:	0.10.7
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/watchdog/
Source0:	https://files.pythonhosted.org/packages/source/w/watchdog/watchdog-%{version}.tar.gz
# Source0-md5:	2fc0058a2479615392d3a5dc73c18866
Patch0:		watchdog-warnings.patch
URL:		https://pypi.org/project/watchdog/
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-PyYAML >= 3.10
BuildRequires:	python-argh
BuildRequires:	python-pathtools >= 0.1.1
BuildRequires:	python-pytest
BuildRequires:	python-pytest-cov
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python-pathtools >= 0.1.1
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 1:2.7
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Python API and shell utilities to monitor file system events.

%description -l pl.UTF-8
API pythonowe i narzędzia powłoki do monitorowania zdarzeń systemu
plików.

%package apidocs
Summary:	API documentation for Python watchdog module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona watchdog
Group:		Documentation

%description apidocs
API documentation for Python watchdog module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona watchdog.

%prep
%setup -q -n watchdog-%{version}
%patch0 -p1

%build
%py_build

%if %{with tests}
LC_ALL=C.UTF-8 \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS=pytest_cov.plugin \
PYTHONPATH=$(pwd)/src \
%{__python} -m pytest tests
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py_install

%py_postclean

%{__mv} $RPM_BUILD_ROOT%{_bindir}/watchmedo{,-2}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING README.rst
%attr(755,root,root) %{_bindir}/watchmedo-2
%{py_sitescriptdir}/watchdog
%{py_sitescriptdir}/watchdog-%{version}-py*.egg-info

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_modules,_static,*.html,*.js}
%endif
