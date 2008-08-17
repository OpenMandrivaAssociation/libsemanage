%define libsepolver 2.0.11-1
%define libselinuxver 2.0.0-1

Summary: SELinux binary policy manipulation library 
Name: libsemanage
Version: 2.0.27
Release: %mkrel 2
License: GPLv2+
Group: System/Libraries
URL:	http://www.selinuxproject.org
Source0: http://www.nsa.gov/selinux/archives/libsemanage-%{version}.tgz
#Source1: http://www.nsa.gov/selinux/archives/libsemanage-%{version}.tgz.sign
Patch0: libsemanage-rhat.patch
#Provides: libsemanage.so
BuildRequires: bison
BuildRequires: flex
BuildRequires: selinux-devel  >= %{libselinuxver}
BuildRequires: sepol-devel >= %{libsepolver}
BuildRequires: ustr-static-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

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

%package -n %{mklibname semanage 1}
Summary: SELinux binary policy manipulation library
Group: System/Libraries
Provides: semanage = %{version}-%{release}

%description -n %{mklibname semanage 1}
libsemanage provides an API for the manipulation of SELinux binary policies.
It is used by checkpolicy (the policy compiler) and similar tools, as well
as by programs like load_policy that need to perform specific transformations
on binary policies such as customizing policy boolean settings.

%package -n %{mklibname semanage -d}
Summary: Header files and libraries used to build policy manipulation tools
Group: Development/C
Requires: %{mklibname semanage 1} = %{version}-%{release}
Provides: semanage-devel = %{version}-%{release}
Obsoletes: %{mklibname semanage 1 -d}

%description -n %{mklibname semanage -d}
The libsemanage-devel package contains the libraries and header files
needed for developing applications that manipulate binary policies. 

%package -n %{mklibname semanage -d -s}
Summary: Static libraries used to build policy manipulation tools
Group: Development/C
Requires: %{mklibname semanage -d} = %{version}-%{release}
Provides: semanage-static-devel = %{version}-%{release}
Obsoletes: %{mklibname semanage 1 -d -s}

%description -n %{mklibname semanage -d -s}
The libsemanage-devel package contains the static libraries
needed for developing applications that manipulate binary policies. 

%package -n python-semanage
Summary: Python bindings for %{name}
Group: Development/Python
%py_requires -d

%description -n python-semanage
This package contains python bindings for %{name}.

%prep
%setup -q
%patch0 -p1

%build
%{make} clean
%{make} CFLAGS="-fPIC %{optflags}" CC=gcc

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/%{_lib}
mkdir -p ${RPM_BUILD_ROOT}/%{_libdir}
mkdir -p ${RPM_BUILD_ROOT}%{_includedir}
make DESTDIR="${RPM_BUILD_ROOT}" LIBDIR="${RPM_BUILD_ROOT}%{_libdir}" SHLIBDIR="${RPM_BUILD_ROOT}/%{_lib}" install install-pywrap

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{mklibname semanage 1} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{mklibname semanage 1} -p /sbin/ldconfig
%endif

%files -n %{mklibname semanage 1}
%defattr(-,root,root)
%config(noreplace) /etc/selinux/semanage.conf
/%{_lib}/libsemanage.so.1

%files -n %{mklibname semanage -d}
%defattr(-,root,root)
%{_libdir}/libsemanage.so
%dir %{_includedir}/semanage
%{_includedir}/semanage/*.h
%{_mandir}/man3/*

%files -n %{mklibname semanage -d -s}
%defattr(-,root,root)
%{_libdir}/libsemanage.a

%files -n python-semanage
%defattr(-,root,root)
%{_libdir}/python*/site-packages/*
