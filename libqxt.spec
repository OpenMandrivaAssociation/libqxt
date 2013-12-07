%define debug_package %nil
%define major 0
%define libname %mklibname qxt %{major}
%define devname %mklibname -d qxt

Name:		libqxt
Version:	0.6.2
Release:	4
Summary:	Qt extension library
Group:		System/Libraries
License:	CPL or LGPLv2
URL:		http://www.libqxt.org/
Source0:	http://bitbucket.org/libqxt/libqxt/get/v%{version}.tar.bz2
# Fix DSO linking
Patch0:		libqxt-linking.patch
# To support multimedia keys when using clementine
# Patch sent to upstream. They want to reimplement it more cleanly.
# We will use this patch until upstream reimplements it.
# http://dev.libqxt.org/libqxt/issue/75
Patch1:		libqxt-media-keys.patch
# Fix wrong header includes RHBZ#733222
# http://dev.libqxt.org/libqxt/issue/112/wrong-include-in-qxtnetworkh
Patch2:		libqxt-header-fix.patch

BuildRequires:	db-devel
BuildRequires:	pkgconfig(xrandr)
BuildRequires:	openssl-devel
BuildRequires:	qt4-devel

%description
LibQxt, an extension library for Qt, provides a suite of cross-platform
utility classes to add functionality not readily available in the Qt toolkit.

%package -n %{libname}
Summary:    %{summary}
Group:      System/Libraries

%description -n %{libname}
LibQxt, an extension library for Qt, provides a suite of cross-platform
utility classes to add functionality not readily available in the Qt toolkit.

%package -n	%{devname}
Summary:	Development files for %{name}
Group:		Development/C++
Provides:	%{name}-devel
BuildRequires:	pkgconfig(avahi-compat-libdns_sd)
BuildRequires:	pkgconfig(avahi-core)
Requires:	db-devel
Requires:	qt4-devel

%description -n	%{devname}
This package contains libraries and header files for developing applications
that use LibQxt.


%prep
%setup -q -n %{name}-%{name}-v%{version}
%patch0 -p1 -b .linking
%patch1 -p1 -b .mediakeys
%patch2 -p1 -b .includes

# We don't want rpath
sed -i '/RPATH/d' src/qxtlibs.pri

%build
%setup_compile_flags
# Does not use GNU configure
./configure -verbose \
	    -release \
	    -prefix %{_prefix} \
	    -libdir %{_libdir}
	    
#-qmake-bin %{_bindir}/qmake} \
%make


%install
#makeinstall_std
make install INSTALL_ROOT=%{buildroot}

# We are installing these to the proper location
rm -fr %{buildroot}%{_prefix}/doc/

%files -n %{libname}
%{_qt_libdir}/*.so.*

%files -n %{devname}
%doc AUTHORS CHANGES *.txt LICENSE README
%doc examples/
%{_includedir}/Qxt*
%{_qt_libdir}/*.so
%{_qt_plugindir}/designer/*.so
%{_qt_datadir}/mkspecs/features/qxt*.prf
