Summary:	ggaoed - ATA over Ethernet target implementation for Linux
Name:		ggaoed
Version:	1.1
Release:	1
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://ggaoed.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	9d46d1b274e96547bb93bc5360a1db54
Source1:	%{name}.init
Source2:	%{name}.sysconfig
Patch0:		%{name}-build.patch
URL:		http://code.google.com/p/ggaoed/
BuildRequires:	docbook2X >= 0.8
BuildRequires:	glib2-devel >= 2.12
BuildRequires:	libaio-devel >= 0.3.107
BuildRequires:	libatomic_ops >= 1.2
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
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
install -d $RPM_BUILD_ROOT%{_sharedstatedir}/ggaoed

%{__make} install \
	datarootdir=$RPM_BUILD_ROOT%{_datadir} \
	sbindir=$RPM_BUILD_ROOT%{_sbindir} \
	mandir=$RPM_BUILD_ROOT%{_mandir}

install -D ggaoed.conf.dist $RPM_BUILD_ROOT%{_sysconfdir}/ggaoed.conf
install -D %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/ggaoed
install -D %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/ggaoed

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add ggaoed
/sbin/chkconfig ggaoed off
%service ggaoed restart

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del ggaoed
	%service ggaoed stop
	# nuke config cache if uninstalling
	rm -rf %{_sharedstatedir}/ggaoed/*
fi

%files
%defattr(644,root,root,755)
%doc NEWS README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ggaoed.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/ggaoed
%attr(754,root,root) /etc/rc.d/init.d/ggaoed
%attr(755,root,root) %{_sbindir}/ggaoectl
%attr(755,root,root) %{_sbindir}/ggaoed
%{_mandir}/man5/ggaoed.conf.5*
%{_mandir}/man8/ggaoectl.8*
%{_mandir}/man8/ggaoed.8*
%dir %{_sharedstatedir}/ggaoed
