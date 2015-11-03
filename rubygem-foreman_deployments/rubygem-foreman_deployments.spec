# This package contains macros that provide functionality relating to
# Software Collections. These macros are not used in default
# Fedora builds, and should not be blindly copied or enabled.
# Specifically, the "scl" macro must not be defined in official Fedora
# builds. For more information, see:
# http://docs.fedoraproject.org/en-US/Fedora_Contributor_Documentation/1/html/Software_Collections_Guide/index.html

%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

%global gem_name foreman_deployments

%define rubyabi 1.9.1
%global foreman_dir /usr/share/foreman
%global foreman_bundlerd_dir %{foreman_dir}/bundler.d

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 0.0.1
Release: 1%{?foremandist}%{?dist}
Summary: A plugin adding Multi-Host Deployment support into the Foreman
Group: Applications/System
License: GPLv3
URL: https://github.com/theforeman/foreman_deployments
Source0: http://rubygems.org/downloads/%{gem_name}-%{version}.gem

Requires: foreman >= 1.8.0

Requires: %{?scl_prefix}rubygem(foreman-tasks) >= 0.7.3
Requires: %{?scl_prefix}rubygem(safe_yaml)
%if 0%{?fedora} > 18
Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
BuildRequires: %{?scl_prefix_ruby}ruby(release)
%else
Requires: %{?scl_prefix_ruby}ruby(abi) >= %{rubyabi}
Requires: %{?scl_prefix_ruby}rubygems
BuildRequires: %{?scl_prefix_ruby}ruby(abi) >= %{rubyabi}
%endif
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}rubygems
BuildRequires: foreman-plugin >= 1.8.0
BuildRequires: %{?scl_prefix}rubygem(foreman-tasks) >= 0.7.3
BuildRequires: %{?scl_prefix}rubygem(safe_yaml)

BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}
Provides: foreman-plugin-deployments

%description
A plugin adding Foreman Multi-Host Deployment support.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}.

%prep
%{?scl:scl enable %{scl} "}
gem unpack %{SOURCE0}
%{?scl:"}

%setup -q -D -T -n  %{gem_name}-%{version}
mkdir -p .%{gem_dir}
%{?scl:scl enable %{scl} "}
gem install --local --install-dir .%{gem_dir} \
            --force %{SOURCE0} --no-rdoc --no-ri
%{?scl:"}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{foreman_bundlerd_dir}

%foreman_bundlerd_file
%foreman_precompile_plugin -s

%files
%dir %{gem_instdir}
%{gem_libdir}
%{gem_instdir}/.tx
%{gem_instdir}/app
%{gem_instdir}/db
%{gem_instdir}/config
%{gem_instdir}/locale
%exclude %{gem_cache}
%{gem_spec}
%{foreman_bundlerd_plugin}
%doc %{gem_instdir}/LICENSE
%{foreman_assets_plugin}

%exclude %{gem_instdir}/test
%exclude %{gem_instdir}/.rubo*

%files doc
%doc %{gem_instdir}/LICENSE
%doc %{gem_instdir}/README.md

%posttrans
# We need to run the db:migrate
%foreman_db_migrate
/usr/sbin/foreman-rake db:seed  >/dev/null 2>&1 || :
/usr/sbin/foreman-rake apipie:cache  >/dev/null 2>&1 || :
%foreman_restart
exit 0

%changelog
* Tue Nov 03 2015 Ondrej Prazak <oprazak@redhat.com> - 0.0.1-1
- Initial package
