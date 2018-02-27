%ruby_version		%(%{__ruby} -rrbconfig -e 'print RbConfig::CONFIG["ruby_version"]')

%ruby_archdir		%(%{__ruby} -rrbconfig -e 'print RbConfig::CONFIG["archdir"]')
%ruby_libdir		%(%{__ruby} -rrbconfig -e 'print RbConfig::CONFIG["rubylibdir"]')
%ruby_sitedir		%(%{__ruby} -rrbconfig -e 'print RbConfig::CONFIG["sitedir"]')
%ruby_sitearchdir	%(%{__ruby} -rrbconfig -e 'print RbConfig::CONFIG["sitearchdir"]')
%ruby_sitelibdir	%(%{__ruby} -rrbconfig -e 'print RbConfig::CONFIG["sitelibdir"]')
%ruby_vendordir		%(%{__ruby} -rrbconfig -e 'print RbConfig::CONFIG["vendordir"]')
%ruby_vendorarchdir	%(%{__ruby} -rrbconfig -e 'print RbConfig::CONFIG["vendorarchdir"]')
%ruby_vendorlibdir	%(%{__ruby} -rrbconfig -e 'print RbConfig::CONFIG["vendorlibdir"]')
%ruby_gemdir		%(%{__ruby} -rrbconfig -e 'print RbConfig::CONFIG["rubygemsdir"]')
%ruby_ridir		%(%{__ruby} -rrbconfig -e 'print RbConfig::CONFIG["ridir"])')

# For ruby packages we want to filter out any provides caused by private
# libs in %%{ruby_vendorarchdir}/%%{ruby_sitearchdir}.
#
# Note that this must be invoked in the spec file, preferably as
# "%{?ruby_default_filter}", before any %description block.
%ruby_default_filter %{expand: \
%global __provides_exclude_from %{?__provides_exclude_from:%{__provides_exclude_from}|}^(%{ruby_vendorarchdir}|%{ruby_sitearchdir})/.*\\\\.so$ \
}
