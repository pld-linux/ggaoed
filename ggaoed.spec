Summary:	ggaoed - ATA over Ethernet target implementation for Linux
Name:		ggaoed
Version:	1.1
Release:	0.1
License:	GPL v2
Group:		Base/Utilities
Source0:	http://ggaoed.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	9d46d1b274e96547bb93bc5360a1db54
Patch0:		%{name}-build.patch
URL:		http://code.google.com/p/ggaoed/
BuildRequires:	docbook2X >= 0.8
BuildRequires:	glib2-devel >= 2.12
BuildRequires:	libaio-devel >= 0.3.107
BuildRequires:	libatomic_ops >= 1.2
Requires:	uname(release) >= 2.6.31
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ggaoed is an AoE (ATA over Ethernet) target implementation for Linux.
It utilizes Linux kernel AIO, memory mapped sockets and other Linux
features to provide the best performance.

%prep
%setup -q
%patch0 -p1

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}

%{__make} install \
	datarootdir=$RPM_BUILD_ROOT%{_datadir} \
	sbindir=$RPM_BUILD_ROOT%{_sbindir} \
	mandir=$RPM_BUILD_ROOT%{_mandir}

install ggaoed.conf.dist $RPM_BUILD_ROOT%{_sysconfdir}/ggaoed.conf

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc NEWS README
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ggaoed.conf
%attr(755,root,root) %{_sbindir}/ggaoectl
%attr(755,root,root) %{_sbindir}/ggaoed
%{_mandir}/man5/ggaoed.conf.5*
%{_mandir}/man8/ggaoectl.8*
%{_mandir}/man8/ggaoed.8*
