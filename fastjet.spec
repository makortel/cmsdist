### RPM external fastjet 3.1.0
%define tag b22035e7b44afb596fce6d393139b59b8bb00d47
%define branch cms/v%realversion
%define github_user cms-externals
Source: git+https://github.com/%github_user/fastjet.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz

%prep
%setup -n %n-%realversion

case %cmsplatf in
    *_gcc4[01234]* ) ;;
    *_armv7hl_* ) CXXFLAGS="-O3 -Wall -ffast-math -std=c++0x -ftree-vectorize" ;;
    * ) CXXFLAGS="-O3 -Wall -ffast-math -std=c++0x -msse3 -ftree-vectorize" ;;
esac


./configure --enable-shared  --enable-atlascone --enable-cmsiterativecone --enable-siscone --prefix=%i --enable-allcxxplugins ${CXXFLAGS+CXXFLAGS="$CXXFLAGS"}

%build
make %makeprocesses

%install
make install
rm -rf %i/lib/*.la
%post
%{relocateConfig}bin/fastjet-config
