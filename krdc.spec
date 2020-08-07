Summary:	KDE Remote Desktop Client
Name:		krdc
Version:	20.08.0
Release:	1
Epoch:		3
License:	GPLv2+
Group:		Graphical desktop/KDE
Url:		http://www.kde.org
%define is_beta %(if test `echo %{version} |cut -d. -f3` -ge 70; then echo -n 1; else echo -n 0; fi)
%if %{is_beta}
%define ftpdir unstable
%else
%define ftpdir stable
%endif
Source0:	http://download.kde.org/%{ftpdir}/release-service/%{version}/src/%{name}-%{version}.tar.xz
Patch0:		krdc-19.04.2-menuentry.patch
BuildRequires:	pkgconfig(libvncserver)
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(KF5DocTools)
BuildRequires:	cmake(KF5Config)
BuildRequires:	cmake(KF5KCMUtils)
BuildRequires:	cmake(KF5DNSSD)
BuildRequires:	cmake(KF5NotifyConfig)
BuildRequires:	cmake(KF5Notifications)
BuildRequires:	cmake(KF5Bookmarks)
BuildRequires:	cmake(KF5IconThemes)
BuildRequires:	cmake(KF5XmlGui)
BuildRequires:	cmake(KF5Completion)
BuildRequires:	cmake(KF5Wallet)
BuildRequires:	cmake(KF5WidgetsAddons)
BuildRequires:	cmake(KF5NotifyConfig)
BuildRequires:	cmake(KF5I18n)
BuildRequires:	cmake(Qt5Core)
BuildRequires:	cmake(Qt5Gui)
BuildRequires:	cmake(Qt5Widgets)
BuildRequires:	cmake(KF5Parts)
BuildRequires:	cmake(KF5WindowSystem)
BuildRequires:	pkgconfig(libssh)
BuildRequires:	freerdp >= 1.0.2
Requires:	freerdp >= 1.0.2
Conflicts:	kde4-filesharing < 3:4.8.0

%description
KDE Remote Desktop Client is a client application that allows you to view
or even control the desktop session on another machine that is running a
compatible server. VNC and RDP are supported.

%files -f %{name}.lang
%dir %{_libdir}/qt5/plugins/krdc
%dir %{_libdir}/qt5/plugins/krdc/kcms
%dir %{_datadir}/kxmlgui5/krdc
%{_bindir}/krdc
%{_libdir}/qt5/plugins/krdc/kcms/*.so
%{_libdir}/qt5/plugins/krdc/*.so
%{_datadir}/applications/org.kde.krdc.desktop
%{_datadir}/config.kcfg/krdc.kcfg
%{_datadir}/kservices5/ServiceMenus/smb2rdc.desktop
%{_datadir}/kservices5/krdc_rdp_config.desktop
%{_datadir}/kservices5/krdc_vnc_config.desktop
%{_datadir}/kservices5/rdp.protocol
%{_datadir}/kservices5/vnc.protocol
%{_datadir}/kxmlgui5/krdc/krdcui.rc
%{_datadir}/metainfo/org.kde.krdc.appdata.xml

#----------------------------------------------------------------------------

%define krdccore_major 5
%define libkrdccore %mklibname krdccore %{krdccore_major}

%package -n %{libkrdccore}
Summary:	Shared library for KRDC
Group:		System/Libraries
Obsoletes:	%{_lib}krdccore1 < 3:4.10.1

%description -n %{libkrdccore}
Shared library for KRDC.

%files -n %{libkrdccore}
%{_libdir}/libkrdccore.so.%{krdccore_major}*
%{_libdir}/libkrdccore.so.%{version}

#----------------------------------------------------------------------------

%define devkrdccore %mklibname krdccore -d

%package -n %{devkrdccore}
Summary:	Development for KRDC
Group:		Development/KDE and Qt
Requires:	%{libkrdccore} = %{EVRD}
Conflicts:	kdenetwork4-devel < 3:4.11.0
Provides:	%{name}-devel = %{EVRD}

%description -n %{devkrdccore}
This package contains header files needed if you want to build applications
based on KRDC.

%files -n %{devkrdccore}
%{_includedir}/krdccore_export.h
%{_includedir}/krdc
%{_libdir}/libkrdccore.so

#----------------------------------------------------------------------------

%prep
%autosetup -p1
%cmake_kde5

%build
%ninja -C build

%install
%ninja_install -C build
%find_lang %{name} --with-html
