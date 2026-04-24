%global debug_package %{nil}
%global __strip /bin/true
%global codename panda3
%global patch    patch1

# Suppress auto-generated Requires/Provides for bundled ELFs under the install
# tree. Android Studio ships Android-bionic libs (libc.so, liblog.so,
# libaaudio.so, libandroid.so, libmediandk.so, libperfetto.so, etc.) used by
# native tools targeting Android — not the host. Without these filters, rpm
# emits unresolvable Requires and dnf install fails.
%global __requires_exclude_from ^%{_libdir}/android-studio/.*$
%global __provides_exclude_from ^%{_libdir}/android-studio/.*$

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
# Directory skeleton
mkdir -p %{buildroot}%{_libdir}/android-studio
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/128x128/apps
mkdir -p %{buildroot}%{_docdir}/%{name}

# Payload: copy entire unpacked tree (preserve perms/symlinks)
cp -a . %{buildroot}%{_libdir}/android-studio/

# Wrapper script
cat > %{buildroot}%{_bindir}/android-studio <<EOF
#!/bin/bash
exec %{_libdir}/android-studio/bin/studio.sh "\$@"
EOF
chmod 0755 %{buildroot}%{_bindir}/android-studio

# Desktop entry
cat > %{buildroot}%{_datadir}/applications/android-studio.desktop <<EOF
[Desktop Entry]
Name=Android Studio
Comment=Official IDE for Android application development
GenericName=Integrated Development Environment
Exec=android-studio %f
Icon=android-studio
Terminal=false
Type=Application
Categories=Development;IDE;
StartupNotify=true
StartupWMClass=jetbrains-studio
MimeType=application/x-extension-iml;
Keywords=android;ide;development;kotlin;java;
EOF

# Icons (from bundled payload inside buildroot — do not re-copy from BUILD)
install -m0644 %{buildroot}%{_libdir}/android-studio/bin/studio.svg \
    %{buildroot}%{_datadir}/icons/hicolor/scalable/apps/android-studio.svg
install -m0644 %{buildroot}%{_libdir}/android-studio/bin/studio.png \
    %{buildroot}%{_datadir}/icons/hicolor/128x128/apps/android-studio.png

# Docs
install -m0644 LICENSE.txt %{buildroot}%{_docdir}/%{name}/LICENSE.txt
cp -a license %{buildroot}%{_docdir}/%{name}/license

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/android-studio.desktop

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database %{_datadir}/applications &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    /usr/bin/update-desktop-database %{_datadir}/applications &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%license %{_docdir}/%{name}/LICENSE.txt
%doc %{_docdir}/%{name}/license
%{_bindir}/android-studio
%{_libdir}/android-studio/
%{_datadir}/applications/android-studio.desktop
%{_datadir}/icons/hicolor/scalable/apps/android-studio.svg
%{_datadir}/icons/hicolor/128x128/apps/android-studio.png

%changelog
* Tue Apr 21 2026 Joakim Lönnegren <joakimlonnegren@gmail.com> - 2025.3.3.7-1
- Initial package for Fedora 43
- Android Studio Panda 3 (2025.3.3.7 Patch 1) from upstream tarball
