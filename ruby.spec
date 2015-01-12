%define _disable_ld_no_undefined 1

%define rubyver 2.2.0
%define subver %(echo %{rubyver}|cut -d. -f1,2)

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
%define gems_dir %{_datadir}/gems
%define rubygems_version 2.4.5
%define rake_ver 10.4.2
%define minitest_ver 5.4.3
%define json_ver 1.8.1
%define rdoc_ver 4.2.0
%define bigdecimal_ver 1.2.6
%define io_console_ver 0.4.3
%define psych_ver 2.0.8
%define test_unit_ver 3.0.8
%define power_assert_ver 0.2.2
#howto properly update ruby from 2.x to 2.y (2.0 to 2.1)
#1. enable bootstrap build
#2. enable gems for bootstrap
#3. disable bootstrap
#3. disable gems
%bcond_without bootstrap
%bcond_without gems
%bcond_with tcltk

Summary:	Object Oriented Script Language

Name:		ruby
Version:	%{rubyver}
Release:	4
License:	Ruby or BSD
Group:		Development/Ruby
Url:		http://www.ruby-lang.org/
Source0:	http://ftp.ruby-lang.org/pub/ruby/%{subver}/ruby-%{rubyver}.tar.gz
Source1:	operating_system.rb
# http://bugs.ruby-lang.org/issues/7807
Patch0: ruby-2.1.0-Prevent-duplicated-paths-when-empty-version-string-i.patch
# Allows to override libruby.so placement. Hopefully we will be able to return
# to plain --with-rubyarchprefix.
# http://bugs.ruby-lang.org/issues/8973
Patch1: ruby-2.1.0-Enable-configuration-of-archlibdir.patch
# Force multiarch directories for i.86 to be always named i386. This solves
# some differencies in build between Fedora and RHEL.
Patch3: ruby-2.1.0-always-use-i386.patch
# Fixes random WEBRick test failures.
# https://bugs.ruby-lang.org/issues/6573.
Patch5: ruby-1.9.3.p195-fix-webrick-tests.patch
# Allows to install RubyGems into custom directory, outside of Ruby's tree.
# http://redmine.ruby-lang.org/issues/5617
Patch8: ruby-2.1.0-custom-rubygems-location.patch
# Make mkmf verbose by default
Patch12: ruby-1.9.3-mkmf-verbose.patch
# Adds support for '--with-prelude' configuration option. This allows to built
# in support for ABRT.
# http://bugs.ruby-lang.org/issues/8566A
# cb - changed in 2.2 and we dont seem to use it
#Patch17: ruby-2.1.0-Allow-to-specify-additional-preludes-by-configuratio.patch
Patch20:	ruby-2.2.0-Do-not-install-to-user-dir.patch

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
%if %{without bootstrap}
BuildRequires:	ruby
Requires:	rubygems
Requires:	ruby(psych)
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
Provides:	ruby-devel = %{version}-%{release}
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
Requires:	ruby-json >= %{json_ver}
Provides:	gem = %{rubygems_version}
Provides:	rubygems = %{rubygems_version}
Provides:	ruby(rubygems) = %{rubygems_version}
BuildArch:	noarch

%description	RubyGems
RubyGems is the Ruby standard for publishing and managing third party
libraries.

%package	rake
Summary:	Simple ruby build program with capabilities similar to make

Group:		Development/Ruby
Version:	%{rake_ver}
Requires:	ruby(abi) = %{subver}
BuildArch:	noarch

%description	rake
Rake is a Make-like program implemented in Ruby. Tasks and dependencies are
specified in standard Ruby syntax.

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


%package	io-console
Summary:	IO/Console is a simple console utilizing library

Group:		Development/Ruby
Version:	%{io_console_ver}
Requires:	ruby(abi) = %{subver}
Requires:	ruby(rubygems) >= %{rubygems_version}

%description	io-console
IO/Console provides very simple and portable access to console. It doesn't
provide higher layer features, such like curses and readline.


%package psych
Summary:	A libyaml wrapper for Ruby

Version:	%{psych_ver}
Group:		Development/Ruby
License:	MIT
Requires:	ruby(abi) = %{subver}
Requires:	ruby(rubygems) >= %{rubygems_version}
Provides:	ruby(psych)
Conflicts:	ruby < 2.0.0

%description	psych
Psych is a YAML parser and emitter. Psych leverages
libyaml[http://pyyaml.org/wiki/LibYAML] for its YAML parsing and emitting
capabilities. In addition to wrapping libyaml, Psych also knows how to
serialize and de-serialize most Ruby objects to and from the YAML format.

%package test-unit
Summary:       Test/unit compatible API testing framework

Version:       %{test_unit_ver}
Group:         Development/Ruby
License:       MIT
Requires:      ruby(abi) = %{subver}
Requires:      ruby(rubygems) >= %{rubygems_version}
Conflicts:     ruby < 2.0.0
BuildArch:     noarch

%package power_assert
Summary:       Power Assert for Ruby

Version:       %{power_assert_ver}
Group:         Development/Ruby
License:       MIT
Requires:      ruby(abi) = %{subver}
Requires:      ruby(rubygems) >= %{rubygems_version}
Conflicts:     ruby < 2.0.0
BuildArch:     noarch

%prep
%setup -qn ruby-%{rubyver}
%apply_patches
# When patching mkmf.rb the mkmf.rb.0010 gets installed
rm lib/mkmf.rb.0*

autoconf

%build
CFLAGS=`echo %{optflags} | sed 's/-fomit-frame-pointer//' | sed 's/-fstack-protector//'`
# use gcc instead of clang
# main reason is ld + clang generates warning
# "missing .note.GNU-stack section implies executable stack"
# in checking LDFLAGS stage and lead to fail
export CC=gcc
export CXX=g++
%ifarch aarch64
export rb_cv_pri_prefix_long_long=ll
%endif
%configure \
	--enable-shared \
	--enable-pthread \
	--with-archlibdir='%{_libdir}' \
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
%if %{without tcltk}
        --with-out-ext=tcl --with-out-ext=tk \
%endif
	--enable-multiarch \
	--with-ruby-version=''

%make

%install
mkdir -p lib/rubygems/defaults
cp %{SOURCE1} lib/rubygems/defaults
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
%if %{without gems}
rm -f %{buildroot}%{_bindir}/{rake,rdoc,ri,testrb}
rm -f %{buildroot}%{_mandir}/man1/{rake,ri}.*
rm -fr %{buildroot}%{ruby_libdir}/{minitest,rake,rdoc,json,bigdecimal,io,test,psych}
rm -fr %{buildroot}%{ruby_libarchdir}/{json,bigdecimal.so,io/console.so,psych.so}
rm -fr %{buildroot}%{_datadir}/gems/{gems,specifications}
rm -f %{buildroot}%{_bindir}/gem
rm -fr %{buildroot}%{rubygems_dir}/rbconfig
rm -fr %{buildroot}%{rubygems_dir}/rubygems
rm -f %{buildroot}%{rubygems_dir}/rubygems.rb
rm -f %{buildroot}%{rubygems_dir}/ubygems.rb
%else
rm -fr  %{buildroot}%{gems_dir}/cache
find %{buildroot}%{gems_dir} -type d -exec chmod 755 {} \;
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
%{ruby_libdir}/digest
%{ruby_libdir}/drb
%{ruby_libdir}/fiddle
%{ruby_libdir}/matrix
%{ruby_libdir}/net
%{ruby_libdir}/openssl
%{ruby_libdir}/optparse
%{ruby_libdir}/racc
%dir %{ruby_libdir}/rbconfig
%dir %{ruby_libarchdir}/rbconfig
%{ruby_libdir}/rexml
%{ruby_libdir}/rinda
%{ruby_libdir}/ripper
%{ruby_libdir}/rss
%{ruby_libdir}/shell
%{ruby_libdir}/syslog
%{ruby_libdir}/unicode_normalize
%{ruby_libdir}/uri
%{ruby_libdir}/webrick
%{ruby_libdir}/xmlrpc
%{ruby_libdir}/yaml
%dir %{ruby_libarchdir}
%{ruby_libarchdir}/continuation.so
%{ruby_libarchdir}/coverage.so
%{ruby_libarchdir}/date_core.so
%{ruby_libarchdir}/dbm.so
%dir %{ruby_libarchdir}/digest
%{ruby_libarchdir}/digest.so
%{ruby_libarchdir}/digest/*.so
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
%{ruby_libarchdir}/rbconfig/sizeof.so
%{ruby_libarchdir}/thread.so
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
%dir %{gems_dir}
%dir %{gems_dir}/gems
%dir %{gems_dir}/specifications
%dir %{gems_dir}/specifications/default
%{rubygems_dir}/rbconfig
%{rubygems_dir}/rubygems
%{rubygems_dir}/rubygems.rb
%{rubygems_dir}/ubygems.rb

%files minitest
%{gems_dir}/gems/minitest-*
%{gems_dir}/specifications/minitest-*.gemspec

%files rake
%{_bindir}/rake
%{_mandir}/man1/rake.1.*
%{ruby_libdir}/rake
%{gems_dir}/gems/rake-*
%{gems_dir}/specifications/default/rake-*.gemspec

%files test-unit
%{gems_dir}/gems/test-unit-*
%{gems_dir}/specifications/test-unit-*.gemspec

%files power_assert
%{gems_dir}/gems/power_assert-*
%{gems_dir}/specifications/power_assert-*.gemspec

%files rdoc
%{_bindir}/rdoc
%{_bindir}/ri
%{ruby_libdir}/rdoc
%{gems_dir}/gems/rdoc-*
%{gems_dir}/specifications/default/rdoc-*.gemspec
%{_mandir}/man1/ri.1.*

%files json
%dir %{ruby_libarchdir}/json
%dir %{ruby_libarchdir}/json/ext
%{ruby_libarchdir}/json/ext/*.so
%{ruby_libdir}/json
%{gems_dir}/specifications/default/json-*.gemspec

%files bigdecimal
%{ruby_libdir}/bigdecimal
%{ruby_libarchdir}/bigdecimal.so
%{gems_dir}/specifications/default/bigdecimal-*.gemspec

%files io-console
%{ruby_libdir}/io
%{ruby_libarchdir}/io/console.so
%{gems_dir}/specifications/default/io-console-*.gemspec

%files psych
%{ruby_libdir}/psych
%{ruby_libarchdir}/psych.so
%{gems_dir}/specifications/default/psych-*.gemspec

%endif
