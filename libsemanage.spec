%define libsepolver %{version}
%define libselinuxver %{version}

# For static libs
%define _disable_lto 1
# Python module
%define _disable_ld_no_undefined 1
# Build system breakage
%undefine _debugsource_packages

Summary: 	SELinux binary policy manipulation library
Name: 		libsemanage
Version: 	3.5
Release: 	2
Epoch:		1
License: 	GPLv2+
Group: 		System/Libraries
URL:		https://www.selinuxproject.org
Source0:	https://github.com/SELinuxProject/selinux/releases/download/%{version}/libsemanage-%{version}.tar.gz
Source1: 	semanage.conf
BuildRequires: 	bison
BuildRequires: 	flex
BuildRequires: 	pkgconfig(libselinux)  >= %{libselinuxver}
BuildRequires: 	pkgconfig(libsepol) >= %{libsepolver}
BuildRequires: 	pkgconfig(ustr)
BuildRequires:  pkgconfig(python3)
BuildRequires: 	pkgconfig(bzip2)
BuildRequires:  pkgconfig(audit)
BuildRequires:	swig

%description
Security-enhanced Linux is a feature of the Linux® kernel and a number
of utilities with enhanced security functionality designed to add
mandatory access controls to Linux.  The Security-enhanced Linux
kernel contains new architectural components originally developed to
improve the security of the Flask operating system. These
architectural components provide general support for the enforcement
of many kinds of mandatory access control policies, including those
based on the concepts of Type Enforcement®, Role-based Access
Control, and Multi-level Security.

libsemanage provides an API for the manipulation of SELinux binary policies.
It is used by checkpolicy (the policy compiler) and similar tools, as well
as by programs like load_policy that need to perform specific transformations
on binary policies such as customizing policy boolean settings.

%package -n %{mklibname semanage}
Summary: 	SELinux binary policy manipulation library
Group: 		System/Libraries
Provides: 	semanage = %{EVRD}

%description -n %{mklibname semanage}
libsemanage provides an API for the manipulation of SELinux binary policies.
It is used by checkpolicy (the policy compiler) and similar tools, as well
as by programs like load_policy that need to perform specific transformations
on binary policies such as customizing policy boolean settings.

%package -n %{mklibname semanage -d}
Summary: 	Header files and libraries used to build policy manipulation tools
Group: 		Development/C
Requires: 	%{mklibname semanage} = %{EVRD}
Provides: 	semanage-devel = %{EVRD}

%description -n %{mklibname semanage -d}
The libsemanage-devel package contains the libraries and header files
needed for developing applications that manipulate binary policies.

%package -n %{mklibname semanage -d -s}
Summary: 	Static libraries used to build policy manipulation tools
Group: 		Development/C
Requires: 	%{mklibname semanage -d} = %{EVRD}
Provides: 	semanage-static-devel = %{EVRD}

%description -n %{mklibname semanage -d -s}
The libsemanage-devel package contains the static libraries
needed for developing applications that manipulate binary policies.

%package -n python-semanage
Summary: 	semanage python bindings for %{name}
Group: 		Development/Python
Provides:	python-%{name} = %{EVRD}
Requires:       semanage = %{EVRD}
Requires:       python%{pyver}dist(selinux)
%rename %{name}-python

%description -n python-semanage
This package contains python bindings for %{name}.

%prep
%autosetup -p1

%build
export LDFLAGS="%{build_ldflags}"

# To support building the Python wrapper against multiple Python runtimes
# Define a function, for how to perform a "build" of the python wrapper against
# a specific runtime:
BuildPythonWrapper() {
  BinaryName=$1

  # Perform the build from the upstream Makefile:
  make \
    CC=%{__cc} \
    PYTHON=$BinaryName \
    CFLAGS="%{optflags}" LIBDIR="%{_libdir}" SHLIBDIR="%{_lib}" \
    pywrap
}

make clean
%make_build CC=%{__cc} CFLAGS="%{optflags}" swigify
%make_build CC=%{__cc} CFLAGS="%{optflags}" LIBDIR="%{_libdir}" SHLIBDIR="%{_lib}" all

BuildPythonWrapper \
  %{__python}
  
%install
InstallPythonWrapper() {
  BinaryName=$1

  make \
    CC=%{__cc} \
    PYTHON=$BinaryName \
    DESTDIR="%{buildroot}" LIBDIR="%{buildroot}%{_libdir}" SHLIBDIR="%{buildroot}%{_libdir}" \
    install-pywrap
}

rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{buildroot}%{_sharedstatedir}/selinux
mkdir -p %{buildroot}%{buildroot}%{_sharedstatedir}/selinux/tmp
make DESTDIR="%{buildroot}" LIBDIR="%{_libdir}" SHLIBDIR="%{_libdir}" install

InstallPythonWrapper \
  %{__python} \
  .so

cp %{SOURCE1} %{buildroot}/etc/selinux/semanage.conf
#ln -sf  %{_libdir}/libsemanage.so.1 %{buildroot}/%{_libdir}/libsemanage.so

%files -n %{mklibname semanage}
%config(noreplace) /etc/selinux/semanage.conf
%{_libdir}/libsemanage.so.2

%files -n %{mklibname semanage -d -s}
%{_libdir}/libsemanage.a

%files -n %{mklibname semanage -d}
%{_libdir}/libsemanage.so
%{_libdir}/pkgconfig/libsemanage.pc
%{_includedir}/semanage
%{_mandir}/man3/*
%{_mandir}/man5/*
%lang(ru) %{_mandir}/ru/man5/semanage.conf.*

%files -n python-semanage
%{python_sitearch}/*.so
%{python_sitearch}/semanage.py*
%{_libexecdir}/selinux/semanage_migrate_store
