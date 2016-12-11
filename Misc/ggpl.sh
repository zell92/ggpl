#!/bin/bash
# ggpl
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color
set -e
echo -e "${RED}Aggiornamento sistema:${NC}"
sudo apt-get update
yes Y | sudo apt-get install software-properties-common
echo -e "${BLUE}Premere un tasto per continuare...${NC}"
read
echo -e "${RED}Installazione git:${NC}"
yes Y | sudo apt install git
echo -e "${RED}Download pyplasm:${NC}"
yes \n | git clone git://github.com/plasm-language/pyplasm.git
echo -e "${BLUE}Premere un tasto per continuare...${NC}"
read
echo -e "${RED}Installazione pyplasm:${NC}"
cd pyplasm
yes Y | sudo apt-get install libfreetype6 libfreetype6-dev libasound2 libasound2-dev alsa-base alsa-utils python python-dev python-setuptools libxinerama-dev libxrender-dev libxcomposite-dev  libxcursor-dev swig libglu1-mesa-dev libfreeimage3 libglew1.10 libpng12-0 libpng12-dev libjpeg-dev libxxf86vm1 libxxf86vm-dev libxi6 libxi-dev libxrandr-dev mesa-common-dev mesa-utils-extra libgl1-mesa-dev libglapi-mesa python-numpy python-scipy libldap2-dev
yes Y | sudo easy_install PyOpenGL PyOpenGL-accelerate
yes \n | sudo add-apt-repository ppa:george-edison55/cmake-3.x
yes Y | sudo apt-get update
yes Y | sudo apt-get install cmake
yes Y | sudo apt-get upgrade
mkdir build
cd build
cmake ../
make
sudo make install # if you get an error try the following "touch install_manifest.txt" and "chmod a+rw ./*"
cd ..
echo -e "${BLUE}Premere un tasto per continuare...${NC}"
read
echo -e "${RED}Download poly2tri:${NC}"
yes Y\n | git clone git://github.com/davidcarne/poly2tri.python
cd poly2tri.python
echo -e "${RED}Installazione larlib:${NC}"
yes Y | python get-pip.py
yes Y | sudo apt-get -y install python-pip
yes Y | sudo pip install --upgrade pip
yes Y | sudo pip install Cython
yes Y | python setup.py build_ext -i
yes Y | sudo python setup.py install
yes Y | sudo pip install larlib
echo -e "${BLUE}Premere un tasto per continuare...${NC}"
read
echo -e "${RED}Installazione software aggiuntivo:${NC}"
yes \n |sudo add-apt-repository ppa:inkscape.dev/stable
sudo apt-get update
echo -e "${RED}Inkscape:${NC}"
yes Y | sudo apt-get install inkscape
echo -e "${RED}Jupyter:${NC}"
yes Y | sudo pip install jupyter
echo -e "${RED}Sublime:${NC}"
yes Y | sudo add-apt-repository ppa:webupd8team/sublime-text-3
yes Y | sudo apt-get update
yes Y | sudo apt-get install sublime-text-installer
cd ..
rm -rf pyplasm/
rm -rf poly2tri.python/
echo -e "${BLUE}FINE${NC}"
echo -e "${BLUE}Premere un tasto per continuare...${NC}"
read
