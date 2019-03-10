#
# Conditional build:
%bcond_without	python		# Python module
%bcond_without	verbose		# verbose build (V=1)

Summary:	The Device Tree Compiler
Summary(pl.UTF-8):	Kompilator drzewiastej struktury urządzeń
Name:		dtc
Version:	1.5.0
Release:	1
License:	GPL v2+ (dtc), GPL v2+ or BSD (fdt library)
Group:		Libraries
Source0:	https://www.kernel.org/pub/software/utils/dtc/%{name}-%{version}.tar.xz
# Source0-md5:	1e7f54238d991b81c54fb5aabf71ff23
Patch0:		%{name}-python.patch
URL:		http://www.devicetree.org/Device_Tree_Compiler
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%if %{with python}
BuildRequires:	python-devel >= 2
BuildRequires:	swig-python
%endif
Requires:	libfdt = %{version}-%{release}
Obsoletes:	dtc-doc < 1.3.0-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Summary:	Python binding for fdt library
Summary(pl.UTF-8):	Wiązanie Pythona do biblioteki fdt
License:	GPL v2+ or BSD
Group:		Libraries/Python

%description -n python-libfdt
Python binding for fdt library.

%description -n python-libfdt -l pl.UTF-8
Wiązanie Pythona do biblioteki fdt.

%prep
%setup -q
%patch0 -p1

%build
%{__make} \
	%{?with_verbose:V=1} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fPIC" \
	%{!?with_python:NO_PYTHON=1}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	%{?with_verbose:V=1} \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir} \
	%{!?with_python:NO_PYTHON=1} \
	SETUP_PREFIX=%{_prefix}

%if %{with python}
%py_postclean
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
%attr(755,root,root) %{_libdir}/libfdt-%{version}.so
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

%if %{with python}
%files -n python-libfdt
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/_libfdt.so
%{py_sitedir}/libfdt.py[co]
%{py_sitedir}/libfdt-%{version}-py*.egg-info
%endif
