#define git 20240218
%define gitbranch release/24.02
%define gitbranchd %(echo %{gitbranch} |sed -e "s,/,-,g")

%define krdccore_major 5
%define libkrdccore %mklibname krdccore

Summary:	KDE Remote Desktop Client
Name:		plasma6-krdc
Version:	24.08.1
Release:	%{?git:0.%{git}.}1
License:	GPLv2+
Group:		Graphical desktop/KDE
Url:		https://www.kde.org
%define is_beta %(if test `echo %{version} |cut -d. -f3` -ge 70; then echo -n 1; else echo -n 0; fi)
%if %{is_beta}
%define ftpdir unstable
%else
%define ftpdir stable
%endif
%if 0%{?git:1}
Source0:	https://invent.kde.org/network/krdc/-/archive/%{gitbranch}/krdc-%{gitbranchd}.tar.bz2#/krdc-%{git}.tar.bz2
%else
Source0:	https://download.kde.org/%{ftpdir}/release-service/%{version}/src/krdc-%{version}.tar.xz
%endif
Patch0:		krdc-19.04.2-menuentry.patch
BuildRequires:	pkgconfig(libvncserver)
BuildRequires:	cmake(ECM)
BuildRequires:	cmake(KF6DocTools)
BuildRequires:	cmake(KF6Config)
BuildRequires:	cmake(KF6KCMUtils)
BuildRequires:	cmake(KF6DNSSD)
BuildRequires:	cmake(KF6NotifyConfig)
BuildRequires:	cmake(KF6Notifications)
BuildRequires:	cmake(KF6Bookmarks)
BuildRequires:	cmake(KF6IconThemes)
BuildRequires:	cmake(KF6XmlGui)
BuildRequires:	cmake(KF6Completion)
BuildRequires:	cmake(KF6StatusNotifierItem)
BuildRequires:	cmake(KF6Wallet)
BuildRequires:	cmake(KF6WidgetsAddons)
BuildRequires:	cmake(KF6NotifyConfig)
BuildRequires:	cmake(KF6I18n)
BuildRequires:	cmake(Qt6Core)
BuildRequires:	cmake(Qt6Gui)
BuildRequires:	cmake(Qt6Widgets)
BuildRequires:	cmake(KF6Parts)
BuildRequires:	cmake(KF6WindowSystem)
BuildRequires:  cmake(Qt6Qml)
BuildRequires:  cmake(Qt6QmlCore)
BuildRequires:  cmake(Qt6QmlNetwork)
BuildRequires:	cmake(PlasmaActivities)
BuildRequires:	pkgconfig(libssh)
BuildRequires:	cmake(FreeRDP) < 3.0
Requires:	%{libkrdccore} = %{EVRD}

%description
KDE Remote Desktop Client is a client application that allows you to view
or even control the desktop session on another machine that is running a
compatible server. VNC and RDP are supported.

%files -f krdc.lang
%dir %{_libdir}/qt6/plugins/krdc
%dir %{_libdir}/qt6/plugins/krdc/kcms
%{_bindir}/krdc
%{_libdir}/qt6/plugins/krdc/kcms/*.so
%{_libdir}/qt6/plugins/krdc/*.so
%{_datadir}/applications/org.kde.krdc.desktop
%{_datadir}/config.kcfg/krdc.kcfg
%{_datadir}/metainfo/org.kde.krdc.appdata.xml
%{_datadir}/qlogging-categories6/krdc.categories

#----------------------------------------------------------------------------

%package -n %{libkrdccore}
Summary:	Shared library for KRDC
Group:		System/Libraries

%description -n %{libkrdccore}
Shared library for KRDC.

%files -n %{libkrdccore}
%{_libdir}/libkrdccore.so.*

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
%autosetup -p1 -n krdc-%{?git:%{gitbranchd}}%{!?git:%{version}}
%cmake \
	-DQT_MAJOR_VERSION=6 \
	-DKDE_INSTALL_USE_QT_SYS_PATHS:BOOL=ON \
	-G Ninja || :
if ! [ -e build.ninja ]; then
	echo cmake failed
	echo CMakeOutput.log:
	echo ================
	cat CMakeFiles/CMakeOutput.log
	echo CMakeError.log:
	echo ===============
	cat CMakeFiles/CMakeError.log
fi

%build
%ninja -C build

%install
%ninja_install -C build
%find_lang krdc --with-html
