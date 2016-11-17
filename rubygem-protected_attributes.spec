%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from protected_attributes-1.0.3.gem by gem2rpm -*- rpm-spec -*-
%global gem_name protected_attributes

Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 1.1.0
Release: 3%{?dist}
Summary: Protect attributes from mass assignment in Active Record models
Group: Development/Languages
License: MIT
URL: https://github.com/rails/protected_attributes
Source0: https://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/rails/protected_attributes.git && cd protected_attributes && git checkout v1.1.0
# tar czvf protected_attributes-1.1.0-tests.tgz test/
Source1: %{gem_name}-%{version}-tests.tgz
# Tests are using already defined class names ('superclass mismatch for class')
Patch0: rubygem-protected_attributes-rename-task-and-firm-models.patch

Requires:      %{?scl_prefix_ruby}ruby(release)
Requires:      %{?scl_prefix_ruby}ruby(rubygems)
Requires:      %{?scl_prefix}rubygem(activemodel) >= 4.0.1
Requires:      %{?scl_prefix}rubygem(activemodel) < 5.0
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
BuildRequires: %{?scl_prefix}rubygem(activerecord)
BuildRequires: %{?scl_prefix}rubygem(mocha)
BuildRequires: %{?scl_prefix}rubygem(railties)
BuildRequires: %{?scl_prefix}rubygem(sqlite3)
BuildArch:     noarch
Provides:      %{?scl_prefix}rubygem(%{gem_name}) = %{version}

# Explicitly require runtime subpackage, as long as older scl-utils do not generate it
Requires: %{?scl_prefix}runtime

%description
Protect attributes from mass assignment.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}.

%prep
%{?scl:scl enable %{scl} - << \EOF}
gem unpack %{SOURCE0}
%{?scl:EOF}

%setup -q -D -T -n  %{gem_name}-%{version}

%{?scl:scl enable %{scl} - << \EOF}
gem spec %{SOURCE0} -l --ruby > %{gem_name}.gemspec
%{?scl:EOF}

%build
# Create the gem as gem install only works on a gem file
%{?scl:scl enable %{scl} - << \EOF}
gem build %{gem_name}.gemspec
%{?scl:EOF}

# %%gem_install compiles any C extensions and installs the gem into ./%%gem_dir
# by default, so that we can move it into the buildroot in %%install
%{?scl:scl enable %{scl} - << \EOF}
%gem_install
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
%{?scl:scl enable %{scl} - << \EOF}
set -e
pushd .%{gem_instdir}
tar xzvf %{SOURCE1}

patch -p1 -F 0 < %{PATCH0}

# Remove Bundler. It just complicates everything.
sed -i "/require 'bundler\/setup'/ s/^/#/" test/test_helper.rb

ruby -Ilib:test -e 'Dir.glob "./test/**/*_test.rb", &method(:require)'
popd
%{?scl:EOF}

%files
%dir %{gem_instdir}
%{gem_instdir}/LICENSE.txt
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md

%changelog
* Wed Apr 06 2016 Pavel Valena <pvalena@redhat.com> - 1.1.0-3
- Add scl macros

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Jun 25 2015 Vít Ondruch <vondruch@redhat.com> - 1.1.0-1
- Update to protected_attributes 1.1.0.

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Jun 18 2014 Vít Ondruch <vondruch@redhat.com> - 1.0.8-1
- Updated to protected_attributes 1.0.8.

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Aug 16 2013 Vít Ondruch <vondruch@redhat.com> - 1.0.3-1
- Initial package
