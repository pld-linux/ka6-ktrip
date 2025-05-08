#
# Conditional build:
%bcond_with	tests		# test suite

%define		kdeappsver	25.04.1
%define		kframever	6.13.0
%define		qtver		6.8
%define		kaname		ktrip
Summary:	Ktrip
Name:		ka6-%{kaname}
Version:	25.04.1
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	7a3fe40641281569b1983447eecdd381
URL:		https://apps.kde.org/itinerary/
BuildRequires:	Qt6Test-devel
BuildRequires:	Qt6Widgets-devel >= 5.15.2
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-tools
BuildRequires:	ka6-kpublictransport-devel >= %{kdeappsver}
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-kcrash-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kirigami-addons-devel >= 0.11.0
BuildRequires:	kf6-qqc2-desktop-style-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	python3
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	shared-mime-info >= 1.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
BuildRequires:	zlib-devel
Obsoletes:	ka5-itinerary < 24
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KTrip is a public transport assistant targeted towards mobile Linux
and Android.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%find_lang %{kaname} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post

%postun
%update_desktop_database_postun

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%doc README.md
%attr(755,root,root) %{_bindir}/ktrip
%{_desktopdir}/org.kde.ktrip.desktop
%{_iconsdir}/hicolor/scalable/apps/org.kde.ktrip.svg
%{_datadir}/metainfo/org.kde.ktrip.appdata.xml
