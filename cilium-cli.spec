%global debug_package %{nil}
%global __strip /bin/true

Name:           cilium-cli
Version:        0.19.2
Release:        1%{?dist}
Summary:        CLI to install, manage and troubleshoot Kubernetes clusters running Cilium

License:        Apache-2.0
URL:            https://github.com/cilium/cilium-cli
Source0:        https://github.com/cilium/cilium-cli/releases/download/v%{version}/cilium-linux-amd64.tar.gz

ExclusiveArch:  x86_64

%description
Cilium CLI is a command-line tool to install, manage, and troubleshoot
Kubernetes clusters running Cilium. Cilium provides eBPF-based networking,
security, and observability for cloud-native environments.

%prep
%setup -q -c

%build
# Nothing to build - this is a pre-built binary

%install
mkdir -p %{buildroot}%{_bindir}
install -m755 cilium %{buildroot}%{_bindir}/cilium

%files
%{_bindir}/cilium

%changelog
* Thu Feb 26 2026 Joakim Lönnegren <joakimlonnegren@gmail.com> - 0.19.2-1
- Initial package for Fedora
- Built from upstream release v0.19.2
