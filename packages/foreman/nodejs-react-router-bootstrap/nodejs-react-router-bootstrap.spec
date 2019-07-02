%global npm_name react-router-bootstrap

Name: nodejs-react-router-bootstrap
Version: 0.24.4
Release: 1%{?dist}
Summary: Integration between React Router and React-Bootstrap
License: Apache-2.0
Group: Development/Libraries
URL: https://github.com/react-bootstrap/react-router-bootstrap
Source0: https://registry.npmjs.org/react-router-bootstrap/-/react-router-bootstrap-0.24.4.tgz
Source1: https://registry.npmjs.org/prop-types/-/prop-types-15.7.2.tgz
Source2: https://registry.npmjs.org/loose-envify/-/loose-envify-1.4.0.tgz
Source3: https://registry.npmjs.org/object-assign/-/object-assign-4.1.1.tgz
Source4: https://registry.npmjs.org/react-is/-/react-is-16.8.6.tgz
Source5: https://registry.npmjs.org/js-tokens/-/js-tokens-4.0.0.tgz
Source6: %{name}-%{version}-registry.npmjs.org.tgz
BuildRequires: nodejs-packaging
BuildArch: noarch
ExclusiveArch: %{nodejs_arches} noarch

Provides: npm(%{npm_name}) = %{version}
Provides: bundled(npm(js-tokens)) = 4.0.0
Provides: bundled(npm(loose-envify)) = 1.4.0
Provides: bundled(npm(object-assign)) = 4.1.1
Provides: bundled(npm(prop-types)) = 15.7.2
Provides: bundled(npm(react-is)) = 16.8.6
Provides: bundled(npm(react-router-bootstrap)) = 0.24.4
AutoReq: no
AutoProv: no

%define npm_cache_dir /tmp/npm_cache_%{name}-%{version}-%{release}

%description
%{summary}

%prep
mkdir -p %{npm_cache_dir}
for tgz in %{sources}; do
  echo $tgz | grep -q registry.npmjs.org || npm cache add --cache %{npm_cache_dir} $tgz
done
%setup -T -q -a 6 -D -n %{npm_cache_dir}

%build
npm install --cache-min Infinity --cache %{npm_cache_dir} --no-shrinkwrap --no-optional --global-style true %{npm_name}@%{version}

%install
mkdir -p %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr node_modules/%{npm_name}/node_modules %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr node_modules/%{npm_name}/lib %{buildroot}%{nodejs_sitelib}/%{npm_name}
cp -pfr node_modules/%{npm_name}/package.json %{buildroot}%{nodejs_sitelib}/%{npm_name}

%clean
rm -rf %{buildroot} %{npm_cache_dir}

%files
%{nodejs_sitelib}/%{npm_name}
%license node_modules/%{npm_name}/LICENSE
%doc node_modules/%{npm_name}/CHANGELOG.md
%doc node_modules/%{npm_name}/README.md

%changelog
* Tue Jul 02 2019 vagrant 0.24.4-1
- Update to 0.24.4

* Wed Sep 12 2018 Bryan Kearney <bryan.kearney@gmail.com> - 0.24.4-2
- Use ASL 2.0 instead of Apache 2.0 or Apache-2.0

* Thu Apr 19 2018 Eric D. Helms <ericdhelms@gmail.com> 0.24.4-1
- Add nodejs-react-router-bootstrap generated by npm2rpm using the single strategy

