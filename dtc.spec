# Conditional build:
%bcond_without	verbose		# verbose build (V=1)

Summary:	The Device Tree Compiler
Name:		dtc
Version:	1.1.0
Release:	0.1
License:	GPL v2 (dtc), GPL/BSD (fdt library)
Group:		Libraries
Source0:	http://www.jdl.com/software/%{name}-v%{version}.tgz
# Source0-md5:	46bcff355b60d85bd311fc95b9ff0630
URL:		http://git.jdl.com/gitweb/
BuildRequires:	bison
BuildRequires:	flex
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%{?debug:%define with_verbose 1}

%description
The Device Tree Compiler, dtc, takes as input a device-tree in a given
format and outputs a device-tree in another format. Typically, the
input format is "dts", a human readable source format, and creates a
"dtb", or binary format as output.

%package devel
Summary:	Header files for fdt library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki fdt
Group:		Development/Libraries
# does not require base. see README.license

%description devel
Header files for fdt library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki fdt.

%package static
Summary:	Static fdt library
Summary(pl.UTF-8):	Statyczna biblioteka fdt
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static fdt library.

%description static -l pl.UTF-8
Statyczna biblioteka fdt.

%prep
%setup -q -n %{name}-v%{version}

%build
%{__make} \
	%{?with_verbose:V=1} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	%{?with_verbose:V=1} \
	PREFIX=%{_prefix} \
	LIBDIR=%{_libdir} \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc TODO README.license Documentation/manual.txt
%attr(755,root,root) %{_bindir}/dtc

%files devel
%defattr(644,root,root,755)
%doc README.license
%{_includedir}/fdt.h
%{_includedir}/libfdt.h

%files static
%defattr(644,root,root,755)
%{_libdir}/libfdt.a
