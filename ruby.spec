%define subver 1.8
%define rubyver 1.8.7
%define patchversion p352
%define rel 1
%define arcver %{rubyver}-%{patchversion}
#%define vendorlibbase	%{_prefix}/lib/ruby
%define vendorlibbase	%{_libdir}/ruby
%define vendorarchbase	%{_libdir}/ruby
%define sitelibbase	%{vendorlibbase}/site_ruby
%define sitearchbase	%{vendorarchbase}/site_ruby
%define libname		%mklibname %name

%global	_normalized_cpu	%(echo %{_target_cpu} | sed 's/^ppc/powerpc/;s/i.86/i386/;s/sparcv./sparc/;s/armv.*/arm/')
# Fri Jul 15 21:28:10 2011 +0000
%global	ruby_tk_git_revision	c2dfaa7d40531aef3706bcc16f38178b0c6633ee

Name:		ruby
Version:	%{rubyver}.%{patchversion}
Release:	%mkrel %rel
# Please check if ruby upstream changes this to "Ruby or GPLv2+"
License:	Ruby or GPLv2
URL:		http://www.ruby-lang.org/

BuildRequires:	zlib-devel
BuildRequires:	db5-devel
BuildRequires:	gdbm-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	tcl-devel
BuildRequires:	tk-devel

BuildRequires:	autoconf
BuildRequires:	bison
BuildRequires:	byacc

# Official ruby source release tarball
Source0:	ftp://ftp.ruby-lang.org/pub/%{name}/%{subver}/%{name}-%{arcver}.tar.bz2

# *  git clone http://github.com/ruby/ruby.git
# *  cd ruby
# *  git checkout %%{ruby_tk_git_revision} ext/tk
# *  tar czvf ruby-rev%%{ruby_tk_git_revision}-ext_tk.tar.gz ext/tk
Source100:	ruby-rev%{ruby_tk_git_revision}-ext_tk.tar.gz

# Patches 23, 29, and 33 brought over from ruby 1.8.6
#  (updated to apply against 1.8.7 source)
# If building against a 64bit arch, use 64bit libdir
Patch23:	ruby-1.8.7-p330-multilib.patch
# Mark all i.86 arch's (eg i586, i686, etc) as i386
Patch29:	ruby-1.8.7-always-use-i386.patch
# Use shared libs as opposed to static for mkmf
# See bug 428384
Patch33:	ruby-1.8.7-p249-mkmf-use-shared.patch
# Remove duplicate path entry
# bug 718695
Patch34:	ruby-1.8.7-p352-path-uniq.patch
# Change ruby load path to conform to Fedora/ruby
# library placement (various 1.8.6 patches consolidated into this)
Patch100:	ruby-1.8.7-lib-paths.patch

Summary:	An interpreter of object-oriented scripting language
Group:		Development/Ruby
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

# emacs-23.2.x itself now provides the ruby mode
# And no Provides here
Obsoletes:	%{name}-mode < 1.8.7
# remove old documentation
# And no Provides here
Obsoletes:	%{name}-docs < 1.8.7

%description
Ruby is the interpreted scripting language for quick and easy
object-oriented programming.  It has many features to process text
files and to do system management tasks (as in Perl).  It is simple,
straight-forward, and extensible.


%package	libs
Summary:	Libraries necessary to run Ruby
Group:		Development/Ruby 
# ext/bigdecimal/bigdecimal.{c,h} are under (GPL+ or Artistic) which
# are used for bigdecimal.so
License:	(Ruby or GPLv2) and (GPL+ or Artistic)
Provides:	ruby(abi) = %{subver}
Provides:	libruby = %{version}-%{release}
Obsoletes:	libruby < %{version}-%{release}

%description libs
This package includes the libruby, necessary to run Ruby.


%package	devel
Summary:	A Ruby development environment
Group:		Development/Ruby
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description	devel
Header files and libraries for building a extension library for the
Ruby or an application embedded Ruby.

%package	static
Summary:	Static libraries for Ruby development environment
Group:		Development/Ruby
Requires:	%{name}-devel%{?_isa} = %{version}-%{release}

%description	static
Static libraries for for building a extension library for the
Ruby or an application embedded Ruby.

%package	irb
Summary:	The Interactive Ruby
Group:		Development/Ruby
# No isa specific
Requires:	%{name} = %{version}-%{release}
Provides:	irb = %{version}-%{release}
Obsoletes:	irb < %{version}-%{release}
BuildArch:	noarch

%description irb
The irb is acronym for Interactive Ruby.  It evaluates ruby expression
from the terminal.


%package	rdoc
Summary:	A tool to generate documentation from Ruby source files
Group:		Development/Ruby
# generators/template/html/html.rb is under CC-BY
License:	(GPLv2 or Ruby) and CC-BY
# No isa specific
Requires:	%{name}-irb = %{version}-%{release}
Provides:	rdoc = %{version}-%{release}
Obsoletes:	rdoc < %{version}-%{release}
BuildArch:	noarch

%description rdoc
The rdoc is a tool to generate the documentation from Ruby source files.
It supports some output formats, like HTML, Ruby interactive reference (ri),
XML and Windows Help file (chm).


%package	ri
Summary:	Ruby interactive reference
Group:		Development/Ruby 
## ruby-irb requires ruby, which ruby-rdoc requires
#Requires: %%{name} = %%{version}-%%{release}
# No isa specific
Requires:	%{name}-rdoc = %{version}-%{release}
Provides:	ri = %{version}-%{release}
Obsoletes:	ri < %{version}-%{release}
# FIXME: Make ruby-ri really arch independent
# BuildArch:	noarch # Currently commented out

%description ri
ri is a command line tool that displays descriptions of built-in
Ruby methods, classes and modules. For methods, it shows you the calling
sequence and a description. For classes and modules, it shows a synopsis
along with a list of the methods the class or module implements.

##
## ruby-tcltk
##
%package	tk
Summary:	Tcl/Tk interface for scripting language Ruby
Group:		Development/Ruby
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}

%description tk
Tcl/Tk interface for the object-oriented scripting language Ruby.

%prep
%setup -q -c -a 100
pushd %{name}-%{arcver}
%patch23 -p1
%patch29 -p1
%patch33 -p1
%patch34 -p1
%patch100 -p1

( 
	cd ext
	rm -rf tk
	cp -a ../../ext/tk tk
	find tk -type d -name \.svn | sort -r | xargs rm -rf

# Remove rpath
	sed -i.rpath -e 's|-Wl,-R|-L|g' tk/extconf.rb
) 

popd
sed -i.redirect	-e '\@RUBY@s@\.rb >@\.rb | cat >@' %{name}-%{arcver}/ext/dl/depend

%build
pushd %{name}-%{arcver}
for i in config.sub config.guess; do
	test -f %{_datadir}/libtool/$i && cp -p %{_datadir}/libtool/$i .
done
autoconf

rb_cv_func_strtod=no
export rb_cv_func_strtod

# bug 489990
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing"
export CFLAGS

%configure \
	--with-default-kcode=none \
	--enable-shared \
	--enable-pthread \
	--disable-rpath \
	--with-readline-include=%{_includedir}/readline5 \
	--with-readline-lib=%{_libdir}/readline5 \
	--with-sitedir='%{sitelibbase}' \
	--with-sitearchdir='%{sitearchbase}' \
	--with-vendordir='%{vendorlibbase}' \
	--with-vendorarchdir='%{vendorarchbase}'

# For example ext/socket/extconf.rb uses try_run (for getaddrinfo test),
# which executes conftest and setting LD_LIBRARY_PATH for libruby.so is
# needed.
export LD_LIBRARY_PATH=$(pwd)

make RUBY_INSTALL_NAME=ruby \
	COPY="cp -p" \
	%{?_smp_mflags}
%ifarch ia64
# Miscompilation? Buggy code?
rm -f parse.o
make OPT=-O0 RUBY_INSTALL_NAME=ruby \
	%{?_smp_mflags}
%endif

# Avoid multilib conflict on -libs (bug 649174)
# Maybe dlconfig.rb is unneeded anyway, however for now moving
# dlconfig.rb and add wrapper (need checking)
CONFIGARCH=$(./miniruby -rrbconfig -e "puts Config::CONFIG['arch']")
[ -z "$CONFIGARCH" ] && exit 1
pushd ext/dl
mkdir $CONFIGARCH
mv dlconfig.rb $CONFIGARCH/
cat > dlconfig.rb <<EOF
require 'rbconfig'
dlconfig_path=File.join(File.dirname(__FILE__), Config::CONFIG['arch'], 'dlconfig')
require dlconfig_path
EOF
popd


# Generate ri doc
rm -rf .ext/rdoc
rm -rf ./RI_TMPDIR
mkdir ./RI_TMPDIR
make \
	DESTDIR=$(pwd)/RI_TMPDIR \
	install-doc

popd

%check
pushd %{name}-%{arcver}
%ifarch ppc64
make test || true
%else
make test
%endif
popd

%install
# install documenation in tmp directory to be
# picked up by %%doc macros in %%files sections
rm -rf tmp-ruby-docs
mkdir tmp-ruby-docs
pushd tmp-ruby-docs

mkdir \
	ruby ruby-libs ruby-tk irb

# First gather all samples
cp -a  ../%{name}-%{arcver}/sample/ ruby
cp -a \
	../%{name}-%{arcver}/lib/README* ../%{name}-%{arcver}/doc/ \
	ruby-libs
# Use tar to keep directory hierarchy
cd ruby-libs
(
	cd ../../%{name}-%{arcver} ; \
	find ext \
	-mindepth 1 \
	\( -path '*/sample/*' -o -path '*/demo/*' \) -o \
	\( -name '*.rb' -not -path '*/lib/*' -not -name extconf.rb \) -o \
	\( -name 'README*' -o -name '*.txt*' -o -name 'MANUAL*' \) \
	\
	| xargs tar cf -
) \
	| tar xf -
cd ..

# make sure that all doc files are the world-readable 
find -type f | xargs chmod 0644

# Fix shebang
grep -rl '#![ \t]*%{_prefix}/local/bin' . | \
	xargs sed -i -e '1s|\(#![ \t]*\)%{_prefix}/local/bin|\1%{_bindir}|'
grep -rl '#![ \t]*\./ruby' . | \
	xargs sed -i -e '1s|\(#![ \t]*\)\./ruby|%{_bindir}/ruby|'

# Fix encoding
# Suppress message
set +x
find . -type f | while read f ; do
	file $f | grep -q 'text' || continue
	iconv -f UTF-8 -t UTF-8 $f &> /dev/null && continue
	for encoding in \
		EUC-JP ISO-8859-1
	do
		iconv -f $encoding -t UTF-8 $f -o $f.tmp 2>/dev/null && \
			{ touch -r $f $f.tmp ; mv $f.tmp $f ; \
				echo -e "$f\t: converted from $encoding -t UTF-8" ; continue 2; } || \
			rm -f $f.tmp
	done
done
# Enable message
set -x

# irb
mv ruby-libs/doc/irb/* irb
rm -rf ruby-libs/doc/irb

# tcltk
mv ruby-libs/ext/tk/* ruby-tk/
rmdir ruby-libs/ext/tk

## Fix encodings
pushd ruby-tk
cd sample
find . -path ./demos-jp/\*.rb -or -path ./tkoptdb\*.rb -or -path ./msgs_rb2/ja.msg | \
	xargs sed -i -e 's|euc-jp|utf-8|'
sed -i \
	-e '/KCODE =/s|euc|utf-8|' -e 's|EUC-JP|UTF-8|' \
	demos-jp/widget
cd ..
sed -i -e 's|EUC-JP|UTF-8|' README.1st
popd

# done w/ docs
popd

# installing binaries ...
make \
	-C $RPM_BUILD_DIR/%{name}-%{version}/%{name}-%{arcver} \
	DESTDIR=$RPM_BUILD_ROOT \
	install

# install ri doc
cp -a ./%{name}-%{arcver}/RI_TMPDIR/* $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{sitelibbase}/%{subver}
mkdir -p $RPM_BUILD_ROOT%{sitearchbase}/%{subver}/%{_normalized_cpu}-%{_target_os}

# remove shebang
for i in \
	$RPM_BUILD_ROOT%{vendorlibbase}/%{subver}/{abbrev,generator,irb/{cmd/subirb,ext/save-history},matrix,rdoc/{markup/sample/rdoc2latex,parsers/parse_rb},set,tsort}.rb; \
	do
	sed -i -e '/^#!.*/,1D' $i
done
# The following can be executable
chmod 0755 $RPM_BUILD_ROOT%{vendorlibbase}/%{subver}/tkextlib/pkg_checker.rb
chmod 0644 $RPM_BUILD_ROOT%{vendorarchbase}/%{subver}/%{_normalized_cpu}-%{_target_os}/*.h

find $RPM_BUILD_ROOT/ -name "*.so" -exec chmod 755 {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-, root, root, -)
%doc	%{name}-%{arcver}/COPYING*
%doc	%{name}-%{arcver}/ChangeLog
%doc	%{name}-%{arcver}/GPL
%doc	%{name}-%{arcver}/LEGAL
%doc	%{name}-%{arcver}/LGPL
%doc	%{name}-%{arcver}/NEWS
%doc	%{name}-%{arcver}/README
%lang(ja)	%doc	%{name}-%{arcver}/README.ja
%doc	%{name}-%{arcver}/ToDo
%doc	tmp-ruby-docs/ruby/*
%{_bindir}/ruby
%{_bindir}/erb
%{_bindir}/testrb
%{_mandir}/man1/ruby.1*

%files	devel
%defattr(-, root, root, -)
%doc	%{name}-%{arcver}/COPYING*
%doc	%{name}-%{arcver}/ChangeLog
%doc	%{name}-%{arcver}/GPL
%doc	%{name}-%{arcver}/LEGAL
%doc	%{name}-%{arcver}/LGPL
%doc	%{name}-%{arcver}/README.EXT
%lang(ja)	%doc	%{name}-%{arcver}/README.EXT.ja
%{_libdir}/libruby.so
%{vendorarchbase}/%{subver}/%{_normalized_cpu}-%{_target_os}/*.h

%files	static
%defattr(-, root, root, -)
%{_libdir}/libruby-static.a

%files	libs
%defattr(-, root, root, -)
%doc %{name}-%{arcver}/README
%lang(ja)	%doc	%{name}-%{arcver}/README.ja
%doc	%{name}-%{arcver}/COPYING*
%doc	%{name}-%{arcver}/ChangeLog
%doc	%{name}-%{arcver}/GPL
%doc	%{name}-%{arcver}/LEGAL
%doc	%{name}-%{arcver}/LGPL
%doc	tmp-ruby-docs/ruby-libs/*
%dir	%{vendorlibbase}
%dir	%{vendorlibbase}/%{subver}
%{sitelibbase}
%ifarch ppc64 s390x sparc64 x86_64
%dir	%{vendorarchbase}
%dir	%{vendorarchbase}/%{subver}
%dir	%{vendorarchbase}/%{subver}/%{_normalized_cpu}-%{_target_os}
%{sitearchbase}
%else
%dir	%{vendorlibbase}/%{subver}/%{_normalized_cpu}-%{_target_os}
%endif
## the following files should goes into ruby-tcltk package.
%exclude	%{vendorlibbase}/%{subver}/*tk.rb
%exclude	%{vendorlibbase}/%{subver}/tcltk.rb
%exclude	%{vendorlibbase}/%{subver}/tk
%exclude	%{vendorlibbase}/%{subver}/tk*.rb
%exclude	%{vendorlibbase}/%{subver}/tkextlib
%exclude	%{vendorarchbase}/%{subver}/%{_normalized_cpu}-%{_target_os}/tcltklib.so
%exclude	%{vendorarchbase}/%{subver}/%{_normalized_cpu}-%{_target_os}/tkutil.so
## the following files should goes into ruby-rdoc package.
%exclude	%{vendorlibbase}/%{subver}/rdoc
## the following files should goes into ruby-irb package.
%exclude	%{vendorlibbase}/%{subver}/irb.rb
%exclude	%{vendorlibbase}/%{subver}/irb
## files in ruby-libs from here
%{vendorlibbase}/%{subver}/*.rb
%{vendorlibbase}/%{subver}/bigdecimal
%{vendorlibbase}/%{subver}/cgi
%{vendorlibbase}/%{subver}/date
%{vendorlibbase}/%{subver}/digest
%{vendorlibbase}/%{subver}/dl
%{vendorlibbase}/%{subver}/drb
%{vendorlibbase}/%{subver}/io
%{vendorlibbase}/%{subver}/net
%{vendorlibbase}/%{subver}/openssl
%{vendorlibbase}/%{subver}/optparse
%{vendorlibbase}/%{subver}/racc
%{vendorlibbase}/%{subver}/rexml
%{vendorlibbase}/%{subver}/rinda
%{vendorlibbase}/%{subver}/rss
%{vendorlibbase}/%{subver}/runit
%{vendorlibbase}/%{subver}/shell
%{vendorlibbase}/%{subver}/soap
%{vendorlibbase}/%{subver}/test
%{vendorlibbase}/%{subver}/uri
%{vendorlibbase}/%{subver}/webrick
%{vendorlibbase}/%{subver}/wsdl
%{vendorlibbase}/%{subver}/xmlrpc
%{vendorlibbase}/%{subver}/xsd
%{vendorlibbase}/%{subver}/yaml
%{_libdir}/libruby.so.*
%{vendorarchbase}/%{subver}/%{_normalized_cpu}-%{_target_os}/*.so
%{vendorarchbase}/%{subver}/%{_normalized_cpu}-%{_target_os}/digest
%{vendorarchbase}/%{subver}/%{_normalized_cpu}-%{_target_os}/io
%{vendorarchbase}/%{subver}/%{_normalized_cpu}-%{_target_os}/racc
%{vendorarchbase}/%{subver}/%{_normalized_cpu}-%{_target_os}/rbconfig.rb

%files tk
%defattr(-, root, root, -)
%doc	%{name}-%{arcver}/COPYING*
%doc	%{name}-%{arcver}/ChangeLog
%doc	%{name}-%{arcver}/GPL
%doc	%{name}-%{arcver}/LEGAL
%doc	%{name}-%{arcver}/LGPL
%doc	tmp-ruby-docs/ruby-tk/*
%{vendorlibbase}/%{subver}/*-tk.rb
%{vendorlibbase}/%{subver}/tcltk.rb
%{vendorlibbase}/%{subver}/tk
%{vendorlibbase}/%{subver}/tk*.rb
%{vendorlibbase}/%{subver}/tkextlib
%{vendorarchbase}/%{subver}/%{_normalized_cpu}-%{_target_os}/tcltklib.so
%{vendorarchbase}/%{subver}/%{_normalized_cpu}-%{_target_os}/tkutil.so

%files	rdoc
%defattr(-, root, root, -)
%doc	%{name}-%{arcver}/COPYING*
%doc	%{name}-%{arcver}/ChangeLog
%doc	%{name}-%{arcver}/GPL
%doc	%{name}-%{arcver}/LEGAL
%doc	%{name}-%{arcver}/LGPL
%{_bindir}/rdoc
%{vendorlibbase}/%{subver}/rdoc

%files irb
%defattr(-, root, root, -)
%doc	%{name}-%{arcver}/COPYING*
%doc	%{name}-%{arcver}/ChangeLog
%doc	%{name}-%{arcver}/GPL
%doc	%{name}-%{arcver}/LEGAL
%doc	%{name}-%{arcver}/LGPL
%doc	tmp-ruby-docs/irb/*
%{_bindir}/irb
%{vendorlibbase}/%{subver}/irb.rb
%{vendorlibbase}/%{subver}/irb

%files ri
%defattr(-, root, root, -)
%doc	%{name}-%{arcver}/COPYING*
%doc	%{name}-%{arcver}/ChangeLog
%doc	%{name}-%{arcver}/GPL
%doc	%{name}-%{arcver}/LEGAL
%doc	%{name}-%{arcver}/LGPL
%{_bindir}/ri
%{_datadir}/ri
