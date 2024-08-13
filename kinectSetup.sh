#!/bin/bash

echo "Initiating kinect setup"
sudo apt-get install -s synaptic
sudo apt-get install -s git cmake freeglut3-dev pkg-config build-essential libxmu-dev libxi-dev libusb-1.0-0-dev 
git clone http://github.com/OpenKinect/libfreenect.git
mv libfreenect $HOME
cd $HOME/libfreenect
mkdir $HOME/libfreenect/build
cd build
cmake ..
make
sudo make install
sudo ldconfig /usr/local/lib64/
sudo adduser $USER video