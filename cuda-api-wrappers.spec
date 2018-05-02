### RPM external cuda-api-wrappers 20180502
#%define tag fe0f79bd6ed2c25efb7b1ada19e9718f5299971e
#%define branch master
#%define github_user cms-externals
%define tag f1b1db2cc4912d68a5da0fb964c2232804db25b3
%define branch master
%define github_user eyalroz


Source: git+https://github.com/%{github_user}/%{n}.git?obj=%{branch}/%{tag}&export=%{n}-%{realversion}&output=/%{n}-%{realversion}.tgz
Requires: cuda cub
BuildRequires: cmake
AutoReqProv: no

# include .a files
%define keep_archives true

%prep
%setup -q -n %{n}-%{realversion}

%build
mkdir build
cd build
cmake .. \
  -DCUDA_TOOLKIT_ROOT_DIR=$CUDA_ROOT \
  -DCUDA_SEPARABLE_COMPILATION=ON \
  -DCUDA_TARGET_COMPUTE_CAPABILITY=50 \
  -DCUDA_NVCC_FLAGS=-O2
make VERBOSE=1

%install
find src/ -name '*.cpp' -delete
cp -ar src       %{i}/include
cp -ar build/lib %{i}/lib
