### RPM cms gcc-toolfile 10.0

# gcc has a separate spec file for the generating a
# toolfile because gcc.spec could be not build because of the 
# "--use-system-compiler" option.

Source: none

%prep
%build
%install
mkdir -p %i/etc/scram.d
if [ "X$GCC_ROOT" = X ]
then
    GCC_PATH=`which gcc` || exit 1
    GCC_ROOT=`echo $GCC_PATH | sed -e 's|/bin/gcc||'`
    GCC_VERSION=`gcc -v 2>&1 | grep "gcc version" | sed 's|[^0-9]*\([0-9].[0-9].[0-9]\).*|\1|'` || exit 1
fi

COMPILER_VERSION=`echo %cmsplatf | sed -e 's|.*gcc\([0-9]*\).*|\1|'`
COMPILER_VERSION_MAJOR=`echo %cmsplatf | sed -e 's|.*gcc\([0-9]\).*|\1|'`

# Generate general template for the tool files. Note that on top of
# this template there are some additional cmsplatf-dependent substitutions
# and some overall general substitutions below
case %cmsplatf in
slc4_ia32_gcc4* | slc5_ia32_gcc4* | slc4_amd64_gcc4* | slc5_amd64_gcc4* | slc5onl_ia32_gcc4* )
cat << \EOF_TOOLFILE >%i/etc/scram.d/cxxcompiler
<doc type=BuildSystem::ToolDoc version=1.1>
<tool name=cxxcompiler version=@GCC_VERSION@ type=compiler>
<client>
 <Environment name=GCC_BASE default="@GCC_ROOT@"></Environment>
 <Environment name=GCCBINDIR default="$GCC_BASE/bin"></Environment>
 <Environment name=CXX value="$GCCBINDIR/c++"></Environment>
</client>
<Flags SCRAM_COMPILER_NAME="gcc@COMPILER_VERSION@">
<Flags CCcompiler="gcc@COMPILER_VERSION_MAJOR@">
<Flags MODULEFLAGS="-shared">
<Flags CXXDEBUGFLAG="-g">
<Flags CPPDEFINES="GNU_GCC">
<Flags CPPDEFINES="_GNU_SOURCE">
<Flags CXXSHAREDOBJECTFLAGS="-fPIC">
<Flags CXXFLAGS="-pedantic -ansi -pthread -pipe">
<Flags CXXFLAGS="@GXXOPT@">
<Flags CXXFLAGS="-felide-constructors -fmessage-length=0 -ftemplate-depth-300">
<Flags CXXFLAGS="-Wall -Wno-non-template-friend -Wno-long-long -Wimplicit -Wreturn-type -Wunused -Wparentheses -Werror=array-bounds -Wno-deprecated -Werror=overflow -Werror=return-type -Werror=format-contains-nul -fdiagnostics-show-option">
<Flags LDFLAGS="@LDOPT@">
<Flags CXXSHAREDFLAGS="-Wl,-E">
<Flags SHAREDSUFFIX="so">
<Flags SCRAM_LANGUAGE_TYPE="C++">
<Runtime name=LD_LIBRARY_PATH value="$GCC_BASE/@GXXLIB@" type=path>
<Runtime name=PATH value="$GCC_BASE/bin" type=path>
</tool>
EOF_TOOLFILE
cat << \EOF_TOOLFILE >%i/etc/scram.d/ccompiler
<doc type=BuildSystem::ToolDoc version=1.1>
<tool name=ccompiler version=@GCC_VERSION@ type=compiler>
<client>
 <Environment name=GCC_BASE default="@GCC_ROOT@"></Environment>
 <Environment name=GCCBINDIR value="$GCC_BASE/bin"></Environment>
 <Environment name=CC value="$GCCBINDIR/gcc"></Environment>
</client>
<Flags CDEBUGFLAG="-g">
<Flags CSHAREDOBJECTFLAGS="-fPIC">
<Flags CFLAGS="-pthread">
<Flags CFLAGS="-O2">
<Flags LDFLAGS="-Wl,-E">
<Flags CSHAREDFLAGS="-Wl,-E">
<Flags SCRAM_COMPILER_NAME="gcc@COMPILER_VERSION@">
<Flags SCRAM_LANGUAGE_TYPE="C">
</tool>
EOF_TOOLFILE
cat << \EOF_TOOLFILE >%i/etc/scram.d/f77compiler
<doc type=BuildSystem::ToolDoc version=1.1>
<tool name=f77compiler version=@GCC_VERSION@ type=compiler>
<lib name=gfortran>
<lib name=m>
<client>
 <Environment name=G77_BASE default="@GCC_ROOT@"></Environment>
 <Environment name=FC default="$G77_BASE/bin/gfortran"></Environment>
</client>
<Flags SCRAM_COMPILER_NAME="gcc@COMPILER_VERSION@">
<Flags FFLAGS="-fno-second-underscore -Wunused -Wuninitialized -O2">
<Flags FCO2Flag="-O2">
<Flags FCOPTIMISED="-O2">
<Flags FCDEBUGFLAG="-g">
<Flags FCSHAREDOBJECTFLAGS="-fPIC">
<Flags SCRAM_LANGUAGE_TYPE="FORTRAN">
</tool>
EOF_TOOLFILE
;;
osx104_ppc32_gcc40* | osx104_ia32_gcc40* | osx105* )
cat << \EOF_TOOLFILE >%i/etc/scram.d/cxxcompiler
<doc type=BuildSystem::ToolDoc version=1.1>
<tool name=cxxcompiler version=@GCC_VERSION@ type=compiler>
<client>
 <Environment name=GCC_BASE default="@GCC_ROOT@"></Environment>
 <Environment name=GCCBINDIR default="$GCC_BASE/bin"></Environment>
 <Environment name=CXX value="$GCCBINDIR/c++"></Environment>
</client>
<Flags SCRAM_COMPILER_NAME="gcc40">
<Flags CCcompiler="gcc40">
<Flags MODULEFLAGS=" ">
<Flags CXXDEBUGFLAG="-g">
<Flags CPPDEFINES="GNU_GCC">
<Flags CPPDEFINES="_GNU_SOURCE">
<Flags CXXSHAREDOBJECTFLAGS="-fPIC">
<Flags CXXFLAGS="-pedantic -ansi -pipe">
<Flags CXXFLAGS="-O2">
<Flags CXXFLAGS="-felide-constructors -fmessage-length=0 -ftemplate-depth-300">
<Flags CXXFLAGS="-Wall -Wno-non-template-friend -Wno-long-long -Wimplicit -Wreturn-type -Wunused -Wparentheses">
<Flags LDFLAGS=" ">
<Flags CXXSHAREDFLAGS="-dynamiclib -single_module">
<Flags SHAREDSUFFIX="dylib">
<Flags SCRAM_LANGUAGE_TYPE="C++">
<Runtime name=DYLD_LIBRARY_PATH value="$GCC_BASE/lib" type=path>
<Runtime name=PATH value="$GCC_BASE/bin" type=path>
</tool>
EOF_TOOLFILE
;;
esac

# Specific substitutions to the templates above (default case needed?)
case %cmsplatf in
  slc4_ia32_gcc4* )
    perl -p -i -e "s|\@LDOPT\@|-Wl,-E|g"   %i/etc/scram.d/cxxcompiler
    perl -p -i -e "s|\@GXXLIB\@|lib|g"   %i/etc/scram.d/cxxcompiler
    perl -p -i -e "s|\@GXXOPT\@|-O2 -fvisibility-inlines-hidden|g"  %i/etc/scram.d/cxxcompiler
  ;;
  slc5_ia32_gcc4* | slc5onl_ia32_gcc4* )
    perl -p -i -e "s|\@LDOPT\@|-Wl,-E -Wl,--hash-style=gnu|g"   %i/etc/scram.d/cxxcompiler
    perl -p -i -e "s|\@GXXLIB\@|lib|g"   %i/etc/scram.d/cxxcompiler
    perl -p -i -e "s|\@GXXOPT\@|-O2|g"   %i/etc/scram.d/cxxcompiler
  ;;
  slc4_amd64_gcc4* )
    perl -p -i -e "s|\@LDOPT\@|-Wl,-E|g"   %i/etc/scram.d/cxxcompiler
    perl -p -i -e "s|\@GXXLIB\@|lib64|g" %i/etc/scram.d/cxxcompiler
    perl -p -i -e "s|\@GXXOPT\@|-O2|g"   %i/etc/scram.d/cxxcompiler
  ;;
  slc5_amd64_gcc4* )
    perl -p -i -e "s|\@LDOPT\@|-Wl,-E -Wl,--hash-style=gnu|g"   %i/etc/scram.d/cxxcompiler
    perl -p -i -e "s|\@GXXLIB\@|lib64|g" %i/etc/scram.d/cxxcompiler
    perl -p -i -e "s|\@GXXOPT\@|-O2|g"   %i/etc/scram.d/cxxcompiler
  ;;
esac

# General substitutions
perl -p -i -e "s|\@GCC_ROOT\@|$GCC_ROOT|g;
               s|\@GCC_VERSION\@|$GCC_VERSION|g;
               s|\@COMPILER_VERSION\@|$COMPILER_VERSION|g;
               s|\@COMPILER_VERSION_MAJOR\@|$COMPILER_VERSION_MAJOR|g;                                        
                                        " %i/etc/scram.d/cxxcompiler \
                                          %i/etc/scram.d/ccompiler  \
                                          %i/etc/scram.d/f77compiler
%post
%{relocateConfig}etc/scram.d/cxxcompiler
%{relocateConfig}etc/scram.d/ccompiler
%{relocateConfig}etc/scram.d/f77compiler
