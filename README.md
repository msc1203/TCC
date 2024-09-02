Dependencias:

sudo apt-get install synaptic

sudo apt-get install git cmake freeglut3-dev pkg-config build-essential libxmu-dev libxi-dev libusb-1.0-0-dev 

git clone http://github.com/OpenKinect/libfreenect.git

Build:

cd libfreenect

mkdir build

cd build

cmake ..

make

sudo make install

sudo ldconfig /usr/local/lib64/


Configurando o python:


cd libfreenect/wrappers/python

comentar tudo que tinha a ver com o cython version no setup.py:
pip3 install Cython
![e72df144-f80e-4c40-9b18-4941e0c5adb7](https://github.com/user-attachments/assets/54b6aa04-03e6-4e45-8d20-829e7ea32b8a)

sudo python3 setup.py build_ext --inplace

sudo python3 setup.py install



Testando:

sudo freenect-glview


