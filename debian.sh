#!/bin/bash

sudo apt update -y
sudo apt upgrade -y
sudo apt install synaptic -y
sudo apt install git -y
sudo apt install cmake -y
sudo apt install freeglut3-dev -y
sudo apt install pkg-config -y
sudo apt install build-essential -y
sudo apt install libxmu-dev -y
sudo apt install libxi-dev -y
sudo apt install libusb-1.0-0-dev -y
sudo apt install cython -y

git clone http://github.com/OpenKinect/libfreenect.git
mv libfreenect $HOME
cd $HOME/libfreenect
mkdir $HOME/libfreenect/build
cd build
cmake .. -DBUILD_PYTHON3=ON
make
sudo make install
sudo ldconfig /usr/local/lib/
sudo adduser $USER video


