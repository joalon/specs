%global debug_package %{nil}

Name:           ghidra
Version:        11.3.2
Release:        1%{?dist}
Summary:        Software reverse engineering framework developed by NSA

License:        Apache-2.0
URL:            https://ghidra-sre.org/
Source0:        https://github.com/NationalSecurityAgency/ghidra/releases/download/Ghidra_%{version}_build/ghidra_%{version}_PUBLIC_20250415.zip

# BuildArch not specified - contains arch-specific native libraries
BuildRequires:  unzip
Requires:       java-21-openjdk
Requires:       java-21-openjdk-devel

%description
Ghidra is a software reverse engineering (SRE) framework created and maintained 
by the National Security Agency Research Directorate. This framework includes 
a suite of full-featured, high-end software analysis tools that enable users 
to analyze compiled code on a variety of platforms including Windows, macOS, 
and Linux. Capabilities include disassembly, assembly, decompilation, graphing, 
and scripting, along with hundreds of other features.

%prep
%setup -q -n ghidra_%{version}_PUBLIC

%build
# Nothing to build - this is a binary distribution

%install
# Create installation directory
mkdir -p %{buildroot}%{_libdir}/%{name}

# Copy all Ghidra files, excluding debug info to avoid conflicts
cp -r * %{buildroot}%{_libdir}/%{name}/

# Remove any .debug files that might cause arch conflicts
find %{buildroot}%{_libdir}/%{name} -name "*.debug" -delete || true

# Create wrapper script
mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/ghidra << 'EOF'
#!/bin/bash
export GHIDRA_INSTALL_DIR=%{_libdir}/%{name}
exec %{_libdir}/%{name}/ghidraRun "$@"
EOF

# Make wrapper executable
chmod +x %{buildroot}%{_bindir}/ghidra

# Create desktop entry
mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/ghidra.desktop << 'EOF'
[Desktop Entry]
Name=Ghidra
Comment=Software Reverse Engineering Framework
Exec=ghidra
Icon=ghidra
Terminal=false
Type=Application
Categories=Development;Security;
StartupNotify=true
EOF

# Install icon (check multiple possible locations)
mkdir -p %{buildroot}%{_datadir}/pixmaps
if [ -f support/ghidra.png ]; then
    cp support/ghidra.png %{buildroot}%{_datadir}/pixmaps/ghidra.png
elif [ -f Ghidra/Framework/Generic/src/main/resources/images/GhidraIcon64.png ]; then
    cp Ghidra/Framework/Generic/src/main/resources/images/GhidraIcon64.png %{buildroot}%{_datadir}/pixmaps/ghidra.png
elif [ -f docs/images/GHIDRA_1.png ]; then
    cp docs/images/GHIDRA_1.png %{buildroot}%{_datadir}/pixmaps/ghidra.png
else
    echo "Icon not found"
fi

# Create man page directory and basic man page
mkdir -p %{buildroot}%{_mandir}/man1
cat > %{buildroot}%{_mandir}/man1/ghidra.1 << 'EOF'
.TH GHIDRA 1 "April 2025" "ghidra %{version}" "User Commands"
.SH NAME
ghidra \- Software reverse engineering framework
.SH SYNOPSIS
.B ghidra
[\fIOPTIONS\fR]
.SH DESCRIPTION
Ghidra is a software reverse engineering (SRE) framework created and maintained 
by the National Security Agency Research Directorate. This framework includes 
a suite of full-featured, high-end software analysis tools that enable users 
to analyze compiled code on a variety of platforms.
.SH OPTIONS
See the Ghidra documentation for detailed usage information.
.SH SEE ALSO
Visit https://ghidra-sre.org/ for comprehensive documentation.
EOF

%files
%{_libdir}/%{name}
%{_bindir}/ghidra
%{_datadir}/applications/ghidra.desktop
%{_datadir}/pixmaps/ghidra.png
%{_mandir}/man1/ghidra.1*

%post
# Update desktop database
if [ -x %{_bindir}/update-desktop-database ]; then
    %{_bindir}/update-desktop-database %{_datadir}/applications &> /dev/null || :
fi

%postun
# Update desktop database
if [ -x %{_bindir}/update-desktop-database ]; then
    %{_bindir}/update-desktop-database %{_datadir}/applications &> /dev/null || :
fi

%changelog
* Sun May 25 2025 Joakim Lönnegren <joakimlonnegren@gmail.com> - 11.3.2-1
- Add Ghidra 11.3.2
- Fixed icon installation path issues
- Added desktop integration and wrapper script
- Configured for Fedora 41 with Java 21 dependency
