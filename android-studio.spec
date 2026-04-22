%global debug_package %{nil}
%global __strip /bin/true
%global codename panda3
%global patch    patch1

Name:           android-studio
Version:        2025.3.3.7
Release:        1%{?dist}
Summary:        Official IDE for Android application development

License:        Apache-2.0 AND (GPL-2.0-only WITH Classpath-exception-2.0)
URL:            https://developer.android.com/studio
Source0:        https://redirector.gvt1.com/edgedl/android/studio/ide-zips/%{version}/android-studio-%{codename}-%{patch}-linux.tar.gz

BuildRequires:  desktop-file-utils
BuildRequires:  hicolor-icon-theme

Requires:       glibc
Requires:       libXtst
Requires:       libXrender
Requires:       libXi
Requires:       libXrandr
Requires:       fontconfig
Requires:       freetype
Requires:       mesa-libGL
Requires:       alsa-lib
Requires:       hicolor-icon-theme
Requires:       desktop-file-utils

ExclusiveArch:  x86_64

%description
Android Studio is the official integrated development environment for
Google's Android operating system, built on JetBrains IntelliJ IDEA.
This package contains the pre-built upstream distribution and uses the
bundled JetBrains Runtime (JBR); no system Java is required.

Note: the Android SDK, NDK, and emulator system images are not bundled.
On first launch, Android Studio's Setup Wizard downloads them into the
user's home directory.

%prep
%setup -q -n android-studio

%build
# no build step — upstream ships pre-built binaries

%install
# populated in Task 3

%files
# populated in Task 5

%changelog
* Tue Apr 21 2026 Joakim Lönnegren <joakimlonnegren@gmail.com> - 2025.3.3.7-1
- Initial package for Fedora 43
- Android Studio Panda 3 (2025.3.3.7 Patch 1) from upstream tarball
