# Conditional build:
%bcond_without	verbose		# verbose build (V=1)

Summary:	The Device Tree Compiler
Summary(pl.UTF-8): Kompilator drzewiastej struktury urządzeń
Name:		dtc
Version:	1.3.0
Release:	1
License:	GPL v2 (dtc), GPL/BSD (fdt library)
Group:		Libraries
Source0:	http://www.jdl.com/software/%{name}-v%{version}.tgz
# Source0-md5:	0b94ed452ed3d3b5c1546c27788c416f
URL:		http://git.jdl.com/gitweb/
BuildRequires:	bison
BuildRequires:	flex
Requires:	%{name}-doc = %{version}-%{release}
Requires:	libfdt = %{version}-%{release}
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
Group:		Libraries
Requires:	%{name}-doc = %{version}-%{release}
# does not require base. see README.license

%description -n libfdt
Device tree library.

%description -n libfdt -l pl.UTF-8
Biblioteka drzewiastej struktury urządzeń.

%package -n libfdt-devel
Summary:	Header files for fdt library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki fdt
Group:		Development/Libraries
Requires:	%{name}-doc = %{version}-%{release}
Requires:	libfdt = %{version}-%{release}
Obsoletes:	dtc-devel
# does not require base. see README.license

%description -n libfdt-devel
Header files for fdt library.

%description -n libfdt-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki fdt.

%package -n libfdt-static
Summary:	Static fdt library
Summary(pl.UTF-8):	Statyczna biblioteka fdt
Group:		Development/Libraries
Requires:	libfdt-devel = %{version}-%{release}
Obsoletes:	dtc-static

%description -n libfdt-static
Static fdt library.

%description -n libfdt-static -l pl.UTF-8
Statyczna biblioteka fdt.

%package doc
Summary:        Dtc documentation
Summary(pl.UTF-8):      Dokumentacja dla dtc
Group:          Development/Libraries

%description doc
Dtc package documentation.

%description doc -l pl.UTF-8
Dokumentacja pakietu dtc.

%prep
%setup -q -n %{name}-v%{version}

%build
%{__make} \
	%{?with_verbose:V=1} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -fPIC"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	%{?with_verbose:V=1} \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post -n libfdt -p /sbin/ldconfig
%postun -n libfdt -p /sbin/ldconfig 

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/convert-dtsv0
%attr(755,root,root) %{_bindir}/dtc
%attr(755,root,root) %{_bindir}/dtdiff
%attr(755,root,root) %{_bindir}/ftdump

%files -n libfdt
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfdt-%{version}.so
%attr(755,root,root) %ghost %{_libdir}/libfdt.so.1

%files -n libfdt-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libfdt.so
%{_includedir}/fdt.h
%{_includedir}/libfdt.h

%files -n libfdt-static
%defattr(644,root,root,755)
%{_libdir}/libfdt.a

%files doc
%doc TODO README.license Documentation/manual.txt
