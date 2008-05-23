Summary:	Object Oriented Script Language
Name:		ruby
Version:	1.8.6
%define		patchversion p114
%define		pversion %{?patchversion:-%patchversion}
%define		subver 1.8
# increase the release number, patchversion is here just to make it visible
Release: 	%mkrel 11%patchversion
License:	Ruby or GPLv2
Group:		Development/Ruby
BuildRequires:	autoconf2.5
BuildRequires:	byacc
BuildRequires:	ncurses-devel
BuildRequires:	readline-devel
BuildRequires:	tcl-devel tk-devel
BuildRequires:	db4-devel
BuildRequires:  libgdbm-devel >= 1.8.3
BuildRequires:  openssl-devel
BuildRequires:	zlib1-devel
Obsoletes:	ruby-rexml
Provides:	ruby-rexml

Source0:	ftp://ftp.ruby-lang.org/pub/ruby/ruby-%{version}%{pversion}.tar.bz2
Source1:	http://www.rubycentral.com/faq/rubyfaqall.html.bz2
Source2:	http://dev.rubycentral.com/downloads/files/ProgrammingRuby-0.4.tar.bz2
Source3:	ruby.macros
Patch0:		ruby-lib64.patch
Patch1:		ruby-do-not-use-system-ruby-to-generate-ri-doc.patch
Patch2:		ruby-1.8.5-CVE-2007-5770.patch
Patch25:	ruby-1.8.6.111-gcc43.patch
# Some tk functions are marked "MODULE_SCOPE" in tk-8.5, and gcc-4.3
# enforces(?) that now. Patch from snippets of
# http://svn.ruby-lang.org/cgi-bin/viewvc.cgi/trunk/ext/tk/tcltklib.c?r1=13105&r2=14426
Patch26:	ruby-1.8.6p114-mdv,svn-tk85-gcc43.patch
URL:		http://www.ruby-lang.org/
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-root

%define my_target_cpu %{_target_cpu}
%ifarch ppc
%define my_target_cpu powerpc
%endif
%ifarch ppc64
%define my_target_cpu powerpc64
%endif
%ifarch amd64
%define my_target_cpu x86_64
%endif

%package	doc
Summary:	Documentation for the powerful language Ruby
Group:		Development/Ruby

%package	devel
Summary:	Development file for the powerful language Ruby
Group:		Development/Ruby
Requires:	%{name} = %{version}

%package	tk
Summary:	Tk extension for the powerful language Ruby
Group:		Development/Ruby
Requires:	%{name} = %{version}

%description
Ruby is the interpreted scripting language for quick and
easy object-oriented programming.  It has many features to
process text files and to do system management tasks (as in
Perl).  It is simple, straight-forward, and extensible.

%description	doc
Ruby is the interpreted scripting language for quick and
easy object-oriented programming.  It has many features to
process text files and to do system management tasks (as in
Perl). It is simple, straight-forward, and extensible.

This package contains the Ruby's documentation

%description	devel
Ruby is the interpreted scripting language for quick and
easy object-oriented programming.  It has many features to
process text files and to do system management tasks (as in
Perl). It is simple, straight-forward, and extensible.

This package contains the Ruby's devel files.

%description	tk
Ruby is the interpreted scripting language for quick and
easy object-oriented programming.  It has many features to
process text files and to do system management tasks (as in
Perl). It is simple, straight-forward, and extensible.

This package contains the Tk extension for Ruby.

%prep
%setup -q -n ruby-%{version}%{pversion}
%patch0 -p0 -b .lib64
%patch1 -p0 -b .ri
%patch2 -p0 -b .cve-2007-5770
%patch25 -p1
%patch26 -p1

sed -i -e "s,| sed 's/linux-gnu$/linux/;s/linux-gnu/linux-/',," configure.in

%build
echo '.text' | gcc -shared -o libdummy.so.0 -xassembler - -ltcl -ltk >& /dev/null && {
  if %{_bindir}/ldd libdummy.so.0 | grep -q "lib\(tcl\|tk\).so"; then
    echo "Your tcl/tk is broken, get one with versioning in the libraries."
    exit 1
  fi
  rm -f libdummy.so.0
}

CFLAGS=`echo %optflags | sed 's/-fomit-frame-pointer//'`
%configure2_5x --enable-shared --disable-rpath --enable-pthread
%make


%install
rm -rf %buildroot
%makeinstall_std install-doc

install -d %buildroot%{_docdir}/%{name}-%{version}
cp -a COPYING* ChangeLog README* ToDo sample %buildroot%{_docdir}/%{name}-%{version}
bzcat %{SOURCE1} > %buildroot%{_docdir}/%{name}-%{version}/FAQ.html

install -d %buildroot%{_datadir}/emacs/site-lisp
cp -a misc/ruby-mode.el %buildroot%{_datadir}/emacs/site-lisp

install -d %buildroot%{_sysconfdir}/emacs/site-start.d
cat <<EOF >%buildroot%{_sysconfdir}/emacs/site-start.d/%{name}.el
(autoload 'ruby-mode "ruby-mode" "Ruby editing mode." t)
(add-to-list 'auto-mode-alist '("\\\\.rb$" . ruby-mode))
(add-to-list 'interpreter-mode-alist '("ruby" . ruby-mode))
EOF

(cd %buildroot%{_docdir}/%{name}-%{version} ; tar xfj %{SOURCE2} ; cd Pro*; mv -f html/* . ; rm -rf html xml)

# Make the file/dirs list, filtering out tcl/tk and devel files
( cd %buildroot \
  && find usr/lib/ruby/%{subver} \
          \( -not -type d -printf "/%%p\n" \) \
          -or \( -type d -printf "%%%%dir /%%p\n" \) \
) | egrep -v '/(tcl)?tk|(%{my_target_cpu}-%{_host_os}/.*[ha]$)' > %{name}.list

# Fix scripts permissions and location
find %buildroot sample -type f | file -i -f - | grep text | cut -d: -f1 >text.list
cat text.list | xargs chmod 0644
#  Magic grepping to get only files with '#!' in the first line
cat text.list | xargs grep -n '^#!' | grep ':1:#!' | cut -d: -f1 >shebang.list
cat shebang.list | xargs sed -i -e 's|/usr/local/bin|/usr/bin|; s|\./ruby|/usr/bin/ruby|'
cat shebang.list | xargs chmod 0755


# Install the rpm macros 
mkdir -p %buildroot%{_sysconfdir}/rpm/macros.d
cp %{SOURCE3} %buildroot%{_sysconfdir}/rpm/macros.d
%check
make test

%clean
rm -rf %buildroot

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files -f %{name}.list
%defattr(-, root, root)
%dir %{_docdir}/%{name}-%{version}
%{_docdir}/%{name}-%{version}/README
%{_bindir}/*
%dir %{_prefix}/lib/%{name}/
%{_libdir}/libruby.so.*
%{_prefix}/lib/%{name}/site_ruby
%{_mandir}/*/*
%{_datadir}/emacs/site-lisp/*
%config(noreplace) %{_sysconfdir}/emacs/site-start.d/*
%{_sysconfdir}/rpm/macros.d/%{name}.macros

%files doc
%defattr(-, root, root)
%{_datadir}/ri
%{_docdir}/%{name}-%{version}/COPYING*
%{_docdir}/%{name}-%{version}/ChangeLog
%{_docdir}/%{name}-%{version}/README.*
%{_docdir}/%{name}-%{version}/FAQ.html
%{_docdir}/%{name}-%{version}/ToDo
%{_docdir}/%{name}-%{version}/sample
%{_docdir}/%{name}-%{version}/ProgrammingRuby*

%files devel
%defattr(-, root, root)
%{_prefix}/lib/%{name}/%{subver}/%{my_target_cpu}-%{_target_os}/*.[ah]
%{_libdir}/libruby-static.a
%{_libdir}/libruby.so

%files tk
%defattr(-, root, root)
%{_prefix}/lib/%{name}/%{subver}/%{my_target_cpu}-%{_target_os}/tcltk*
%{_prefix}/lib/%{name}/%{subver}/%{my_target_cpu}-%{_target_os}/tk*
%{_prefix}/lib/%{name}/%{subver}/tcltk*
%{_prefix}/lib/%{name}/%{subver}/tk*
%{_prefix}/lib/%{name}/%{subver}/test/unit/ui/tk

