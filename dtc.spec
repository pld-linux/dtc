#
# Conditional build:
%bcond_without	python		# Python module (any)
%bcond_without	python2		# CPython 2.x module
%bcond_without	python3		# CPython 3.x module
%bcond_without	verbose		# verbose build (V=1)

%if %{without python}
%undefine	with_python2
%undefine	with_python3
%endif
Summary:	The Device Tree Compiler
Summary(pl.UTF-8):	Kompilator drzewiastej struktury urządzeń
Name:		dtc
Version:	1.6.1
Release:	3
License:	GPL v2+ (dtc), GPL v2+ or BSD (fdt library)
Group:		Libraries
Source0:	https://www.kernel.org/pub/software/utils/dtc/%{name}-%{version}.tar.xz
# Source0-md5:	709888bac3aad657e6020d0e491fc0ba
Patch0:		%{name}-python.patch
URL:		https://www.devicetree.org/
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	pkgconfig
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	yaml-devel
%if %{with python}
%if %{with python2}
BuildRequires:	python-devel >= 2
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.2
%endif
BuildRequires:	swig-python >= 2.0.10
%endif
Requires:	libfdt = %{version}-%{release}
Obsoletes:	dtc-doc < 1.3.0-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		abi_ver	%{version}

%{?debug:%define with_verbose 1}

%description
The Device Tree Compiler, dtc, takes as input a device-tree in a given
format and outputs a device-tree in another format. Typically, the
input format is "dts", a human readable source format, and creates a
"dtb", or binary format as output.

%description -l pl.UTF-8
Kompilator drzewiastej struktury urządzeń, dtc, przyjmuje na wejściu
dane w jednym formacie by na wyjściu wyprodukować strukturę danych w
innym. Najczęściej format wejściowy to "dts", intuicyjny i łatwy w
odczycie (tzw. human readable), natomiast wyjściowy to "dtb" lub
inaczej format binarny.

%package -n libfdt
Summary:	Device tree library
Summary(pl.UTF-8):	Biblioteka drzewiastej struktury urządzeń
License:	GPL v2+ or BSD
Group:		Libraries
Obsoletes:	dtc-doc < 1.3.0-2
# does not require base. see README.license

%description -n libfdt
Device tree library.

%description -n libfdt -l pl.UTF-8
Biblioteka drzewiastej struktury urządzeń.

%package -n libfdt-devel
Summary:	Header files for fdt library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki fdt
License:	GPL v2+ or BSD
Group:		Development/Libraries
Requires:	libfdt = %{version}-%{release}
Obsoletes:	dtc-devel
Obsoletes:	dtc-doc < 1.3.0-2

%description -n libfdt-devel
Header files for fdt library.

%description -n libfdt-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki fdt.

%package -n libfdt-static
Summary:	Static fdt library
Summary(pl.UTF-8):	Statyczna biblioteka fdt
License:	GPL v2+ or BSD
Group:		Development/Libraries
Requires:	libfdt-devel = %{version}-%{release}
Obsoletes:	dtc-static

%description -n libfdt-static
Static fdt library.

%description -n libfdt-static -l pl.UTF-8
Statyczna biblioteka fdt.

%package -n python-libfdt
Summary:	Python 2 binding for fdt library
Summary(pl.UTF-8):	Wiązanie Pythona 2 do biblioteki fdt
License:	GPL v2+ or BSD
Group:		Libraries/Python

%description -n python-libfdt
Python 2 binding for fdt library.

%description -n python-libfdt -l pl.UTF-8
Wiązanie Pythona 2 do biblioteki fdt.

%package -n python3-libfdt
Summary:	Python 3 binding for fdt library
Summary(pl.UTF-8):	Wiązanie Pythona 3 do biblioteki fdt
License:	GPL v2+ or BSD
Group:		Libraries/Python

%description -n python3-libfdt
Python 3 binding for fdt library.

%description -n python3-libfdt -l pl.UTF-8
Wiązanie Pythona 3 do biblioteki fdt.

%prep
%setup -q
%patch0 -p1

%build
%{__make} -j1 \
	%{?with_verbose:V=1} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fPIC" \
	NO_PYTHON=1

%if %{with python}
cd pylibfdt
ln -sf ../version_gen.h .
ln -sf ../libfdt .

%if %{with python2}
%py_build
%endif
%if %{with python3}
%py3_build
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -j1 install \
	DESTDIR=$RPM_BUILD_ROOT \
	%{?with_verbose:V=1} \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir} \
	NO_PYTHON=1 \
	SETUP_PREFIX=%{_prefix}

%if %{with python}
cd pylibfdt

%if %{with python2}
%py_install

%py_postclean
%endif
%if %{with python3}
%py3_install
%endif
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n libfdt -p /sbin/ldconfig
%postun	-n libfdt -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README README.license
%attr(755,root,root) %{_bindir}/convert-dtsv0
%attr(755,root,root) %{_bindir}/dtc
%attr(755,root,root) %{_bindir}/dtdiff
%attr(755,root,root) %{_bindir}/fdtdump
%attr(755,root,root) %{_bindir}/fdtget
%attr(755,root,root) %{_bindir}/fdtoverlay
%attr(755,root,root) %{_bindir}/fdtput

%files -n libfdt
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfdt-%{abi_ver}.so
%attr(755,root,root) %ghost %{_libdir}/libfdt.so.1

%files -n libfdt-devel
%defattr(644,root,root,755)
%doc TODO Documentation/manual.txt
%attr(755,root,root) %{_libdir}/libfdt.so
%{_includedir}/fdt.h
%{_includedir}/libfdt.h
%{_includedir}/libfdt_env.h

%files -n libfdt-static
%defattr(644,root,root,755)
%{_libdir}/libfdt.a

%if %{with python2}
%files -n python-libfdt
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_libfdt.so
%{py_sitedir}/libfdt.py[co]
%{py_sitedir}/libfdt-%{abi_ver}*.egg-info
%endif

%if %{with python3}
%files -n python3-libfdt
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/_libfdt.cpython-*.so
%{py3_sitedir}/libfdt.py
%{py3_sitedir}/__pycache__/libfdt.cpython-*.py[co]
%{py3_sitedir}/libfdt-%{abi_ver}*.egg-info
%endif
