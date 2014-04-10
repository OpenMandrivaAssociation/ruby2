%define rubyver 2.0.0
%define subver %(echo %{rubyver}|cut -d. -f1,2)
%define patchversion p451

%define libname %mklibname ruby %{subver}
%define devname %mklibname ruby -d

%define ruby_libdir %{_datadir}/%{name}
%define ruby_libarchdir %{_libdir}/%{name}

# This is the local lib/arch and should not be used for packaging.
%define ruby_sitelibdir %{_datadir}/ruby/site_ruby
%define ruby_sitearchdir %{_libdir}/ruby/site_ruby

# This is the general location for libs/archs compatible with all
# or most of the Ruby versions available in the Fedora repositories.
%define ruby_vendorlibdir %{_datadir}/ruby/vendor_ruby
%define ruby_vendorarchdir %{_libdir}/ruby/vendor_ruby

# The RubyGems library has to stay out of Ruby directory three, since the
# RubyGems should be share by all Ruby implementations.
%define rubygems_dir %{_datadir}/ruby/gems
%define rubygems_version 2.0.2

%bcond_with bootstrap
%bcond_without gems
%bcond_with tcltk

Summary:	Object Oriented Script Language
Name:		ruby
Version:	%{rubyver}.%{patchversion}
Release:	13
License:	Ruby or BSD
Group:		Development/Ruby
Url:		http://www.ruby-lang.org/
Source0:	http://ftp.ruby-lang.org/pub/ruby/%{subver}/ruby-%{rubyver}-%{patchversion}.tar.bz2
Source1:	operating_system.rb
# == FEDORA PATCHES BEGINS ==
# http://bugs.ruby-lang.org/issues/7807
Patch0:		ruby-2.0.0-Prevent-duplicated-paths-when-empty-version-string-i.patch
# Force multiarch directories for i.86 to be always named i386. This solves
# some differencies in build between Fedora and RHEL.
Patch3:		ruby-1.9.3-always-use-i386.patch
# Fixes random WEBRick test failures.
# https://bugs.ruby-lang.org/issues/6573.
Patch5:		ruby-1.9.3.p195-fix-webrick-tests.patch
# Allows to install RubyGems into custom directory, outside of Ruby's tree.
# http://redmine.ruby-lang.org/issues/5617
Patch8:		ruby-1.9.3-custom-rubygems-location.patch
# Add support for installing binary extensions according to FHS.
# https://github.com/rubygems/rubygems/issues/210
# Note that 8th patch might be resolved by
# https://bugs.ruby-lang.org/issues/7897
Patch9:		rubygems-2.0.0-binary-extensions.patch
# Make mkmf verbose by default
Patch12:	ruby-1.9.3-mkmf-verbose.patch
# This slightly changes behavior of "gem install --install-dir" behavior.
# Without this patch, Specifications.dirs is modified and gems installed on
# the system cannot be required anymore. This causes later issues when RDoc
# documentation should be generated, since json gem is sudenly not accessible.
# https://github.com/rubygems/rubygems/pull/452
Patch13:	rubygems-2.0.0-Do-not-modify-global-Specification.dirs-during-insta.patch
# This prevents issues, when ruby configuration specifies --with-ruby-version=''.
# https://github.com/rubygems/rubygems/pull/455
Patch14:	rubygems-2.0.0-Fixes-for-empty-ruby-version.patch
# Adds aarch64 support.
# http://bugs.ruby-lang.org/issues/8331
# https://bugzilla.redhat.com/show_bug.cgi?id=926463
# Please note that this is the BZ patch, it might be good idea to update it
# with its upstream version when available.
Patch16:	ruby-2.0.0-p195-aarch64.patch
# Adds support for '--with-prelude' configuration option. This allows to built
# in support for ABRT.
# http://bugs.ruby-lang.org/issues/8566
Patch17:	ruby-2.1.0-Allow-to-specify-additional-preludes-by-configuratio.patch
# Fixes issues with DESTDIR.
# https://bugs.ruby-lang.org/issues/8115
Patch18:	ruby-2.0.0-p247-Revert-mkmf.rb-prefix-install_dirs-only-with-DESTDIR.patch
# == FEDORA PATCHES ENDS ==
Patch20:	ruby-2.0.0-p451-Do-not-install-to-user-dir.patch
Patch21:	ruby-2.0.0-p451-readline.patch

BuildRequires:	byacc
BuildRequires:	doxygen
BuildRequires:	db-devel
BuildRequires:	gdbm-devel >= 1.8.3
BuildRequires:	readline-devel
BuildRequires:	yaml-devel
BuildRequires:	pkgconfig(ncurses)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(libffi)
%if %{with tcltk}
BuildRequires:	pkgconfig(tcl)
BuildRequires:	pkgconfig(tk)
%endif
%rename	ruby-rexml
# explicit file provides (since such requires are automatically added by find-requires)
Provides:	/usr/bin/ruby
Provides:	ruby(abi) = %subver
%if !%{with bootstrap}
BuildRequires:	ruby
Requires:	rubygems >= %{rubygems_version}
Requires:	rubygem(psych)
Requires:	ruby(irb)
Requires:	ruby(bigdecimal)
%endif

%description
Ruby is the interpreted scripting language for quick and
easy object-oriented programming.  It has many features to
process text files and to do system management tasks (as in
Perl).  It is simple, straight-forward, and extensible.

%package	-n %{libname}
Summary:	Libraries necessary to run Ruby
Group:		Development/Ruby

%description	-n %{libname}
This package includes the shared library for %{name}.

%package	doc
Summary:	Documentation for the powerful language Ruby
Group:		Development/Ruby
BuildArch:	noarch

%description	doc
This package contains the documentation for Ruby.

%package -n	%{devname}
Summary:	Development file for the powerful language Ruby
Group:		Development/Ruby
Requires:	%{name} = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	ruby-devel < 2.0.0.p247-13

%description -n	%{devname}
This package contains the Ruby's devel files.

%if %{with tcltk}
%package	tk
Summary:	Tk extension for the powerful language Ruby
Group:		Development/Ruby
Requires:	%{name} = %{version}

%description	tk
This package contains the Tk extension for Ruby.
%endif

%package	RubyGems
Summary:	The Ruby standard for packaging ruby libraries
Group:		Development/Ruby
Version:	%{rubygems_version}
Requires:	ruby(abi) = %{subver}
Requires:	rdoc
Provides:	gem = %{rubygems_version}
Provides:	rubygems = %{rubygems_version}
Provides:	ruby(rubygems) = %{rubygems_version}
BuildArch:	noarch

%description	RubyGems
RubyGems is the Ruby standard for publishing and managing third party
libraries.

%define rake_ver 0.9.6
%package	rake
Summary:	Simple ruby build program with capabilities similar to make
Group:		Development/Ruby
Version:	%{rake_ver}
Requires:	ruby(abi) = %{subver}
BuildArch:	noarch

%description	rake
Rake is a Make-like program implemented in Ruby. Tasks and dependencies are
specified in standard Ruby syntax.

%define minitest_ver 4.3.2
%package	minitest
Summary:	Minitest provides a complete suite of testing facilities
Group:		Development/Ruby
Version:	%{minitest_ver}
License:	MIT
Requires:	ruby(abi) = %{subver}
Requires:	ruby(rubygems) >= %{rubygems_version}
BuildArch:	noarch

%description	minitest
minitest/unit is a small and incredibly fast unit testing framework.

minitest/spec is a functionally complete spec engine.

minitest/benchmark is an awesome way to assert the performance of your
algorithms in a repeatable manner.

minitest/mock by Steven Baker, is a beautifully tiny mock object
framework.

minitest/pride shows pride in testing and adds coloring to your test
output.

%define json_ver 1.7.7
%package	json
Summary:	This is a JSON implementation as a Ruby extension in C
Group:		Development/Ruby
Version:	%{json_ver}
License:	Ruby or GPLv2
Requires:	ruby(abi) = %{subver}
Requires:	ruby(rubygems) >= %{rubygems_version}

%description	json
This is a implementation of the JSON specification according to RFC 4627.
You can think of it as a low fat alternative to XML, if you want to store
data to disk or transmit it over a network rather than use a verbose
markup language.

%define rdoc_ver 4.0.0
%package	rdoc
Summary:	A tool to generate HTML and command-line documentation for Ruby projects
Group:		Development/Ruby
Version:	%{rdoc_ver}
License:	GPLv2 and Ruby and MIT
Requires:	ruby(abi) = %{subver}
Requires:	ruby(rubygems) >= %{rubygems_version}
Requires:	ruby(irb) = %{version}
Provides:	rdoc = %{rdoc_ver}
Provides:	ri = %{rdoc_ver}
BuildArch:	noarch

%description 	rdoc
RDoc produces HTML and command-line documentation for Ruby projects.  RDoc
includes the 'rdoc' and 'ri' tools for generating and displaying online
documentation.

%package	irb
Summary:	The Interactive Ruby
Group:		Development/Ruby
Provides:	irb = %{version}-%{release}
Provides:	ruby(irb) = %{version}-%{release}
Conflicts:	ruby < 1.9
BuildArch:	noarch

%description	irb
The irb is acronym for Interactive Ruby.  It evaluates ruby expression
from the terminal.

%define bigdecimal_ver 1.2.0
%package	bigdecimal
Summary:	BigDecimal provides arbitrary-precision floating point decimal arithmetic
Group:		Development/Ruby
Version:	%{bigdecimal_ver}
License:	GPL+ or Artistic
Provides:	ruby(bigdecimal)
Requires:	ruby(abi) = %{subver}
Requires:	ruby(rubygems) >= %{rubygems_version}

%description	bigdecimal
Ruby provides built-in support for arbitrary precision integer arithmetic.
For example:

42**13 -> 1265437718438866624512

BigDecimal provides similar support for very large or very accurate floating
point numbers. Decimal arithmetic is also useful for general calculation,
because it provides the correct answers people expect–whereas normal binary
floating point arithmetic often introduces subtle errors because of the
conversion between base 10 and base 2.


%define io_console_ver 0.4.2
%package	io-console
Summary:	IO/Console is a simple console utilizing library
Group:		Development/Ruby
Version:	%{io_console_ver}
Requires:	ruby(abi) = %{subver}
Requires:	ruby(rubygems) >= %{rubygems_version}

%description	io-console
IO/Console provides very simple and portable access to console. It doesn't
provide higher layer features, such like curses and readline.


%define psych_ver 2.0.0
%package psych
Summary:	A libyaml wrapper for Ruby
Version:	%{psych_ver}
Group:		Development/Ruby
Provides:	rubygem(psych)
License:	MIT
Requires:	ruby(abi) = %{subver}
Requires:	ruby(rubygems) >= %{rubygems_version}
Conflicts:	ruby < 2.0.0

%description	psych
Psych is a YAML parser and emitter. Psych leverages
libyaml[http://pyyaml.org/wiki/LibYAML] for its YAML parsing and emitting
capabilities. In addition to wrapping libyaml, Psych also knows how to
serialize and de-serialize most Ruby objects to and from the YAML format.

%define test_unit_ver 2.0.0
%package test-unit
Summary:	test/unit compatible API testing framework
Version:	%{psych_ver}
Group:		Development/Ruby
License:	MIT
Requires:	ruby(abi) = %{subver}
Requires:	ruby(rubygems) >= %{rubygems_version}
Conflicts:	ruby < 2.0.0
BuildArch:	noarch

%prep
%setup -qn ruby-%{rubyver}-%{patchversion}
%apply_patches
# When patching mkmf.rb the mkmf.rb.0010 gets installed
rm lib/mkmf.rb.0*

autoconf

%build
CFLAGS=`echo %optflags | sed 's/-fomit-frame-pointer//'`
%ifarch aarch64
export rb_cv_pri_prefix_long_long=ll
%endif
%configure2_5x \
	--enable-shared \
	--enable-pthread \
	--with-rubylibprefix='%{ruby_libdir}' \
        --with-rubyarchprefix='%{ruby_libarchdir}' \
	--with-sitedir='%{ruby_sitelibdir}' \
	--with-sitearchdir='%{ruby_sitearchdir}' \
	--with-vendordir='%{ruby_vendorlibdir}' \
	--with-vendorarchdir='%{ruby_vendorarchdir}' \
	--with-rubyhdrdir='%{_includedir}' \
        --with-rubyarchhdrdir='$(archincludedir)' \
        --with-sitearchhdrdir='$(sitehdrdir)/$(arch)' \
        --with-vendorarchhdrdir='$(vendorhdrdir)/$(arch)' \
        --with-rubygemsdir='%{rubygems_dir}' \
        --with-ruby-pc='%{name}.pc' \
        --enable-multiarch \
        --with-ruby-version=''
%make

%install
%makeinstall_std install-doc

install -d %{buildroot}%{_datadir}/emacs/site-lisp
cp -a misc/ruby-mode.el %{buildroot}%{_datadir}/emacs/site-lisp

install -d %{buildroot}%{_sysconfdir}/emacs/site-start.d
cat <<EOF >%{buildroot}%{_sysconfdir}/emacs/site-start.d/%{name}.el
(autoload 'ruby-mode "ruby-mode" "Ruby editing mode." t)
(add-to-list 'auto-mode-alist '("\\\\.rb$" . ruby-mode))
(add-to-list 'interpreter-mode-alist '("ruby" . ruby-mode))
EOF

# Install custom operating_system.rb
mkdir -p %{buildroot}%{rubygems_dir}/rubygems/defaults
cp %{SOURCE1} %{buildroot}%{rubygems_dir}/rubygems/defaults

# drop gems if not wanted, so that we could split them out as seperated source rpm
%if !%{with gems}
rm -f %{buildroot}%{_bindir}/{rake,rdoc,ri,testrb}
rm -f %{buildroot}%{_mandir}/man1/{rake,ri}.*
rm -fr %{buildroot}%{ruby_libdir}/{minitest,rake,rdoc,json,bigdecimal,io,test,psych}
rm -fr %{buildroot}%{ruby_libarchdir}/{json,bigdecimal.so,io/console.so,psych.so}
rm -fr %{buildroot}%{rubygems_dir}/{gems,specifications}
rm -f %{buildroot}%{_bindir}/gem
rm -fr %{buildroot}%{rubygems_dir}/rbconfig
rm -fr %{buildroot}%{rubygems_dir}/rubygems
rm -f %{buildroot}%{rubygems_dir}/rubygems.rb
rm -f %{buildroot}%{rubygems_dir}/ubygems.rb
%endif

#% check
#make test

%files
%{_bindir}/erb
%{_bindir}/ruby
%dir %{ruby_libdir}
%{ruby_libdir}/*.rb
%exclude %{ruby_libdir}/irb.rb
%if %{with tcltk}
%exclude %{ruby_libdir}/multi-tk.rb
%exclude %{ruby_libdir}/remote-tk.rb
%exclude %{ruby_libdir}/tcltk.rb
%exclude %{ruby_libdir}/tk.rb
%exclude %{ruby_libdir}/tkafter.rb
%exclude %{ruby_libdir}/tkbgerror.rb
%exclude %{ruby_libdir}/tkcanvas.rb
%exclude %{ruby_libdir}/tkclass.rb
%exclude %{ruby_libdir}/tkconsole.rb
%exclude %{ruby_libdir}/tkdialog.rb
%exclude %{ruby_libdir}/tkentry.rb
%exclude %{ruby_libdir}/tkfont.rb
%exclude %{ruby_libdir}/tkmacpkg.rb
%exclude %{ruby_libdir}/tkmenubar.rb
%exclude %{ruby_libdir}/tkmngfocus.rb
%exclude %{ruby_libdir}/tkpalette.rb
%exclude %{ruby_libdir}/tkscrollbox.rb
%exclude %{ruby_libdir}/tktext.rb
%exclude %{ruby_libdir}/tkvirtevent.rb
%exclude %{ruby_libdir}/tkwinpkg.rb
%endif
%{ruby_libdir}/cgi
%{ruby_libdir}/date
%{ruby_libdir}/digest
%{ruby_libdir}/dl
%{ruby_libdir}/drb
%{ruby_libdir}/fiddle
%{ruby_libdir}/matrix
%{ruby_libdir}/net
%{ruby_libdir}/openssl
%{ruby_libdir}/optparse
%{ruby_libdir}/racc
%{ruby_libdir}/rbconfig
%{ruby_libdir}/rexml
%{ruby_libdir}/rinda
%{ruby_libdir}/ripper
%{ruby_libdir}/rss
%{ruby_libdir}/shell
%{ruby_libdir}/syslog
%{ruby_libdir}/uri
%{ruby_libdir}/webrick
%{ruby_libdir}/xmlrpc
%{ruby_libdir}/yaml
%dir %{ruby_libarchdir}
%{ruby_libarchdir}/continuation.so
%{ruby_libarchdir}/coverage.so
%{ruby_libarchdir}/curses.so
%{ruby_libarchdir}/date_core.so
%{ruby_libarchdir}/dbm.so
%dir %{ruby_libarchdir}/digest
%{ruby_libarchdir}/digest.so
%{ruby_libarchdir}/digest/*.so
%dir %{ruby_libarchdir}/dl
%{ruby_libarchdir}/dl.so
%{ruby_libarchdir}/dl/*.so
%dir %{ruby_libarchdir}/enc
%{ruby_libarchdir}/enc/*.so
%dir %{ruby_libarchdir}/enc/trans
%{ruby_libarchdir}/enc/trans/*.so
%{ruby_libarchdir}/etc.so
%{ruby_libarchdir}/fcntl.so
%{ruby_libarchdir}/fiber.so
%{ruby_libarchdir}/fiddle.so
%{ruby_libarchdir}/gdbm.so
%dir %{ruby_libarchdir}/io
%{ruby_libarchdir}/io/nonblock.so
%{ruby_libarchdir}/io/wait.so
%dir %{ruby_libarchdir}/mathn
%{ruby_libarchdir}/mathn/*.so
%{ruby_libarchdir}/nkf.so
%{ruby_libarchdir}/objspace.so
%{ruby_libarchdir}/openssl.so
%{ruby_libarchdir}/pathname.so
%{ruby_libarchdir}/pty.so
%dir %{ruby_libarchdir}/racc
%{ruby_libarchdir}/racc/*.so
%{ruby_libarchdir}/rbconfig.rb
%{ruby_libarchdir}/readline.so
%{ruby_libarchdir}/ripper.so
%{ruby_libarchdir}/sdbm.so
%{ruby_libarchdir}/socket.so
%{ruby_libarchdir}/stringio.so
%{ruby_libarchdir}/strscan.so
%{ruby_libarchdir}/syslog.so
%{ruby_libarchdir}/zlib.so
%{_mandir}/man1/erb.1.*
%{_mandir}/man1/ruby.1.*
%{_datadir}/emacs/site-lisp/*
%config(noreplace) %{_sysconfdir}/emacs/site-start.d/*
%{_datadir}/ruby/site_ruby
%{_libdir}/ruby/site_ruby
%{_datadir}/ruby/vendor_ruby
%{_libdir}/ruby/vendor_ruby

%files doc
%{_datadir}/ri
%{_datadir}/doc/ruby

%files -n %{libname}
%{_libdir}/libruby.so.%{subver}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/libruby-static.a
%{_libdir}/libruby.so
%{_libdir}/pkgconfig/*.pc

%if %{with tcltk}
%files tk
%{ruby_libarchdir}/tcltklib.so
%{ruby_libarchdir}/tkutil.so
%{ruby_libdir}/multi-tk.rb
%{ruby_libdir}/remote-tk.rb
%{ruby_libdir}/tcltk.rb
%{ruby_libdir}/tk.rb
%{ruby_libdir}/tkafter.rb
%{ruby_libdir}/tkbgerror.rb
%{ruby_libdir}/tkcanvas.rb
%{ruby_libdir}/tkclass.rb
%{ruby_libdir}/tkconsole.rb
%{ruby_libdir}/tkdialog.rb
%{ruby_libdir}/tkentry.rb
%{ruby_libdir}/tkfont.rb
%{ruby_libdir}/tkmacpkg.rb
%{ruby_libdir}/tkmenubar.rb
%{ruby_libdir}/tkmngfocus.rb
%{ruby_libdir}/tkpalette.rb
%{ruby_libdir}/tkscrollbox.rb
%{ruby_libdir}/tktext.rb
%{ruby_libdir}/tkvirtevent.rb
%{ruby_libdir}/tkwinpkg.rb
%{ruby_libdir}/tk
%{ruby_libdir}/tkextlib
%endif

%files irb
%{_bindir}/irb
%{ruby_libdir}/irb.rb
%{ruby_libdir}/irb
%{_mandir}/man1/irb.1*

%if %{with gems}
%files RubyGems
%{_bindir}/gem
%dir %{rubygems_dir}
%{rubygems_dir}/rbconfig
%{rubygems_dir}/rubygems
%{rubygems_dir}/rubygems.rb
%{rubygems_dir}/ubygems.rb

%files minitest
%{ruby_libdir}/minitest
%{rubygems_dir}/specifications/default/minitest-*.gemspec

%files rake
%{_bindir}/rake
%{_mandir}/man1/rake.1.*
%{ruby_libdir}/rake
%{rubygems_dir}/gems/rake-*
%{rubygems_dir}/specifications/default/rake-*.gemspec

%files rdoc
%{_bindir}/rdoc
%{_bindir}/ri
%{ruby_libdir}/rdoc
%{rubygems_dir}/gems/rdoc-*
%{rubygems_dir}/specifications/default/rdoc-*.gemspec
%{_mandir}/man1/ri.1.*

%files json
%dir %{ruby_libarchdir}/json
%dir %{ruby_libarchdir}/json/ext
%{ruby_libarchdir}/json/ext/*.so
%{ruby_libdir}/json
%{rubygems_dir}/specifications/default/json-*.gemspec

%files bigdecimal
%{ruby_libdir}/bigdecimal
%{ruby_libarchdir}/bigdecimal.so
%{rubygems_dir}/specifications/default/bigdecimal-*.gemspec

%files io-console
%{ruby_libdir}/io
%{ruby_libarchdir}/io/console.so
%{rubygems_dir}/specifications/default/io-console-*.gemspec

%files psych
%{ruby_libdir}/psych
%{ruby_libarchdir}/psych.so
%{rubygems_dir}/specifications/default/psych-*.gemspec

%files test-unit
%{_bindir}/testrb
%{ruby_libdir}/test
%{rubygems_dir}/gems/test-unit-*
%{rubygems_dir}/specifications/default/test-unit-*.gemspec
%endif
