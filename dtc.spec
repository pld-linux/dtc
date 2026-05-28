#
# Conditional build:
%bcond_without	python		# Python module (any)
%bcond_without	python3		# CPython 3.x module
%bcond_without	static_libs	# static library

%if %{without python}
%undefine	with_python3
%endif
Summary:	The Device Tree Compiler
Summary(pl.UTF-8):	Kompilator drzewiastej struktury urządzeń
Name:		dtc
Version:	1.8.1
Release:	1
License:	GPL v2+ (dtc), GPL v2+ or BSD (fdt library)
Group:		Libraries
Source0:	https://www.kernel.org/pub/software/utils/dtc/%{name}-%{version}.tar.xz
# Source0-md5:	9753bdbf18763efef1f5ae8c0cecb5f6
URL:		https://www.devicetree.org/
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	meson >= 0.57.0
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	yaml-devel >= 0.2.3
%if %{with python3}
BuildRequires:	python3 >= 1:3.8
BuildRequires:	python3-devel >= 1:3.8
BuildRequires:	python3-modules >= 1:3.8
BuildRequires:	swig-python >= 2.0.10
%endif
Requires:	libfdt = %{version}-%{release}
Requires:	yaml >= 0.2.3
Obsoletes:	dtc-doc < 1.3.0-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Obsoletes:	dtc-devel < 1.3.0
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
Obsoletes:	dtc-static < 1.3.0

%description -n libfdt-static
Static fdt library.

%description -n libfdt-static -l pl.UTF-8
Statyczna biblioteka fdt.

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

%build
%meson \
	%{!?with_static_libs:--default-library=shared} \
	-Dpython=%{__enabled_disabled python}
%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%if %{with python3}
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n libfdt -p /sbin/ldconfig
%postun	-n libfdt -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.license README.md
%attr(755,root,root) %{_bindir}/convert-dtsv0
%attr(755,root,root) %{_bindir}/dtc
%attr(755,root,root) %{_bindir}/dtdiff
%attr(755,root,root) %{_bindir}/fdtdump
%attr(755,root,root) %{_bindir}/fdtget
%attr(755,root,root) %{_bindir}/fdtoverlay
%attr(755,root,root) %{_bindir}/fdtput

%files -n libfdt
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfdt.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libfdt.so.1

%files -n libfdt-devel
%defattr(644,root,root,755)
%doc TODO Documentation/manual.txt
%attr(755,root,root) %{_libdir}/libfdt.so
%{_includedir}/fdt.h
%{_includedir}/libfdt.h
%{_includedir}/libfdt_env.h
%{_pkgconfigdir}/libfdt.pc

%if %{with static_libs}
%files -n libfdt-static
%defattr(644,root,root,755)
%{_libdir}/libfdt.a
%endif

%if %{with python3}
%files -n python3-libfdt
%defattr(644,root,root,755)
%attr(755,root,root) %{py3_sitedir}/_libfdt.cpython-*.so
%{py3_sitedir}/libfdt.py
%{py3_sitedir}/__pycache__/libfdt.cpython-*.py[co]
%endif
