#!/bin/bash
sudo apt-get update
sudo apt-get upgrade

#install some deps
sudo apt-get -y install git vlc-nox cmake libopencv-dev

#build and install ffmpeg
git clone https://github.com/FFmpeg/FFmpeg.git
mv FFmpeg ffmpeg
cd ffmpeg
./configure
make -j5
sudo make install

#pull the modect userland and build the binary
git clone https://github.com/sodnpoo/userland.git
cd userland
mkdir build
cd build
cmake ../
make -j5 opencv_modect

# link in the default mask
ln -s ~/opencv_modect_tools/mask.png ~

# make the drop directory
mkdir ~/drop
