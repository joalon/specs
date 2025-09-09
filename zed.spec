Name:           zed-editor
Version:        0.202.7
Release:        1%{?dist}
Summary:        High-performance, multiplayer code editor

# Disable debug package generation for pre-built binaries
%global debug_package %{nil}
%global __strip /bin/true

License:        GPL-3.0-or-later AND Apache-2.0 AND AGPL-3.0-or-later
URL:            https://zed.dev
Source0:        https://github.com/zed-industries/zed/releases/download/v%{version}/zed-linux-x86_64.tar.gz

# Runtime dependencies based on ldd output and bundled libraries
Requires:       glibc
Requires:       libgcc
Requires:       vulkan-loader
# Desktop integration
Requires:       hicolor-icon-theme
Requires:       desktop-file-utils

# Build dependencies (minimal for binary package)
BuildRequires:  desktop-file-utils
BuildRequires:  hicolor-icon-theme

# Only x86_64 for now as that's what upstream provides
ExclusiveArch:  x86_64

%description
Zed is a high-performance, multiplayer code editor from the creators
of Atom and Tree-sitter, written in Rust. This package contains the
pre-built binaries from the upstream release.

Features:
- Written from scratch in Rust for performance
- GPU-accelerated rendering
- Real-time collaboration
- AI integration capabilities
- Extension system

%prep
%autosetup -n zed.app

%build
# No build needed - using pre-built binaries

%install
# Create directory structure
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libexecdir}/zed-editor
mkdir -p %{buildroot}%{_datadir}/applications
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{512x512,1024x1024}/apps
mkdir -p %{buildroot}%{_libdir}/zed-editor
mkdir -p %{buildroot}%{_docdir}/%{name}

# Install main binaries
install -m755 bin/zed %{buildroot}%{_bindir}/zed
install -m755 libexec/zed-editor %{buildroot}%{_libexecdir}/zed-editor/zed-editor

# Install bundled libraries to avoid conflicts
install -m644 lib/* %{buildroot}%{_libdir}/zed-editor/

# Install desktop file
install -m644 share/applications/zed.desktop %{buildroot}%{_datadir}/applications/

# Install icons
install -m644 share/icons/hicolor/512x512/apps/zed.png %{buildroot}%{_datadir}/icons/hicolor/512x512/apps/
install -m644 share/icons/hicolor/1024x1024/apps/zed.png %{buildroot}%{_datadir}/icons/hicolor/1024x1024/apps/

# Install license documentation
install -m644 licenses.md %{buildroot}%{_docdir}/%{name}/

%check
# Validate desktop file
desktop-file-validate %{buildroot}%{_datadir}/applications/zed.desktop

%post
# Update icon cache
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%license licenses.md
%doc %{_docdir}/%{name}/licenses.md
%{_bindir}/zed
%{_libexecdir}/zed-editor/
%{_libdir}/zed-editor/
%{_datadir}/applications/zed.desktop
%{_datadir}/icons/hicolor/512x512/apps/zed.png
%{_datadir}/icons/hicolor/1024x1024/apps/zed.png

%changelog
* Tue Sep 09 2025 Joakim Lönnegren <joakimlonnegren@gmail.com> - 0.202.7-1
- Initial package for Fedora
- Built from upstream source v0.202.7
