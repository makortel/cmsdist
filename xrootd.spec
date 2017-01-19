### RPM external xrootd 4.6.0
## INITENV +PATH LD_LIBRARY_PATH %i/lib64
%define tag fd9f39b7a9d478607e96a61b071ba93f26d074bb
%define branch master
%define github_user xrootd
Source: git+https://github.com/%github_user/xrootd.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

Patch0: xrootd-gcc7
Patch1: xrootd-add-version

BuildRequires: cmake
Requires: zlib
Requires: openssl

%prep
%setup -n %n-%{realversion}
%patch0 -p1
%patch1 -p1

# need to fix these from xrootd git
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/cleanup.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/loadRTDataToMySQL.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/xrdmonCollector.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/prepareMySQLStats.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/xrdmonCreateMySQL.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/xrdmonLoadMySQL.pl
perl -p -i -e 's|^#!.*perl(.*)|#!/usr/bin/env perl$1|' src/XrdMon/xrdmonPrepareStats.pl

%build
mkdir build
cd build

# By default xrootd has perl, fuse, krb5, readline, and crypto enabled.
# libfuse and libperl are not produced by CMSDIST.
cmake ../ \
  -DCMAKE_INSTALL_PREFIX=%{i} \
  -DOPENSSL_ROOT_DIR:PATH=${OPENSSL_ROOT} \
  -DZLIB_ROOT:PATH=${ZLIB_ROOT} \
  -DENABLE_PYTHON=FALSE \
  -DENABLE_FUSE=FALSE \
  -DENABLE_KRB5=TRUE \
  -DENABLE_READLINE=FALSE \
  -DENABLE_CRYPTO=TRUE \
  -DCMAKE_SKIP_RPATH=TRUE

# Use makeprocess macro, it uses compiling_processes defined by
# build configuration file or build argument
make %makeprocesses VERBOSE=1

%install
cd build
make install
cd ..

%define strip_files %i/lib
%define keep_archives true

