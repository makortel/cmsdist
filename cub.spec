### RPM external cub 1.8.0

Source: https://github.com/NVlabs/cub/archive/1.8.0.zip
Requires: cuda

%prep

#%define __unzip unzip -d %{n}-%{realversion}

%setup -q -n %{n}-%{realversion}

%build

%install
echo $PWD
mkdir -p %{i}/include
cp -ar %{n}-%{realversion}/cub %{i}/include/cub
