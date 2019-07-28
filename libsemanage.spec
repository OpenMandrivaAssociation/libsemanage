%global with_python2 1
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print (get_python_lib(1))")}



%define libsepolver %{version}
%define libselinuxver %{version}


Summary: 	SELinux binary policy manipulation library
Name: 		libsemanage
Version: 	2.9
Release: 	1
Epoch:		1
License: 	GPLv2+
Group: 		System/Libraries
URL:		http://www.selinuxproject.org
Source0:	https://github.com/SELinuxProject/selinux/releases/download/20190315/libsemanage-%{version}.tar.gz
Source1: 	semanage.conf
Patch1:         libsemanage-fedora.patch
BuildRequires: 	bison
BuildRequires: 	flex
BuildRequires: 	pkgconfig(libselinux)  >= %{libselinuxver}
BuildRequires: 	pkgconfig(libsepol) >= %{libsepolver}
BuildRequires: 	pkgconfig(ustr)
BuildRequires:  pkgconfig(python)
BuildRequires: 	pkgconfig(bzip2)
BuildRequires:  pkgconfig(audit)
BuildRequires:	swig
BuildRequires:  pkgconfig(python)

%if 0%{?with_python2}
BuildRequires:  python2
BuildRequires:  pkgconfig(python)
%endif # if with_python2


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
Summary: 	SELinux binary policy manipulation library
Group: 		System/Libraries
Provides: 	semanage = %{EVRD}

%description -n %{mklibname semanage 1}
libsemanage provides an API for the manipulation of SELinux binary policies.
It is used by checkpolicy (the policy compiler) and similar tools, as well
as by programs like load_policy that need to perform specific transformations
on binary policies such as customizing policy boolean settings.

%package -n %{mklibname semanage -d}
Summary: 	Header files and libraries used to build policy manipulation tools
Group: 		Development/C
Requires: 	%{mklibname semanage 1} = %{EVRD}
Provides: 	semanage-devel = %{EVRD}
Obsoletes: 	%{mklibname semanage 1 -d}

%description -n %{mklibname semanage -d}
The libsemanage-devel package contains the libraries and header files
needed for developing applications that manipulate binary policies.

%package -n %{mklibname semanage -d -s}
Summary: 	Static libraries used to build policy manipulation tools
Group: 		Development/C
Requires: 	%{mklibname semanage -d} = %{EVRD}
Provides: 	semanage-static-devel = %{EVRD}
Obsoletes: 	%{mklibname semanage 1 -d -s}

%description -n %{mklibname semanage -d -s}
The libsemanage-devel package contains the static libraries
needed for developing applications that manipulate binary policies.

%package python
Summary: 	semanage python bindings for %{name}
Group: 		Development/Python
Provides:	python-%{name} = %{EVRD}
Requires:       semanage = %{EVRD}
Requires:       libselinux-python
Provides: 	semanage-python = %{EVRD}
## This line could be removed before the release of mga6
## It's needed to remove wrongly name packages
Obsoletes:	python-semanage

%description python
This package contains python bindings for %{name}.

%if 0%{?with_python2}
%package python2
Summary: 	Python bindings for %{name}
Group: 		Development/Python
Requires:       semanage = %{EVRD}
Requires:       libselinux-python2
Provides: 	semanage-python2 = %{EVRD}
Provides:	python2-%{name} = %{EVRD}
## This line could be removed before the release of mga6
## It's needed to remove wrongly name packages
Obsoletes:	python2-semanage


%description python2
The libsemanage-python3 package contains the python 3 bindings for developing
SELinux management applications.
%endif # if with_python2

%prep
%setup -q
%autopatch -p1

%build
export LDFLAGS="%{ldflags}"

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
  %{__python2}
  
%if 0%{?with_python2}
BuildPythonWrapper \
  %{__python3}
%endif # with_python2

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

%if 0%{?with_python2}
InstallPythonWrapper \
  %{__python2} \
  $(python2-config --extension-suffix)
%endif # with_python2
  
cp %{SOURCE1} %{buildroot}/etc/selinux/semanage.conf
ln -sf  %{_libdir}/libsemanage.so.1 %{buildroot}/%{_libdir}/libsemanage.so

%files -n %{mklibname semanage 1}
%config(noreplace) /etc/selinux/semanage.conf
%{_libdir}/libsemanage.so.1

%files -n %{mklibname semanage -d -s}
%{_libdir}/libsemanage.a

%files -n %{mklibname semanage -d}
%{_libdir}/libsemanage.so
%{_libdir}/pkgconfig/libsemanage.pc
%{_includedir}/semanage
%{_mandir}/man3/*
%{_mandir}/man5/*
%{_mandir}/ru/man5/semanage.conf.*

%files  python
%{python_sitearch}/*.so
%{python_sitearch}/semanage.py*
%{python_sitearch}/__pycache__/semanage*
%{_libexecdir}/selinux/semanage_migrate_store

%if 0%{?with_python2}
%files  python2
%{python2_sitearch}/_semanage.so
%{python2_sitearch}/semanage.py*
%endif # if with_python2
