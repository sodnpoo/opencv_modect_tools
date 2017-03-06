#!/bin/bash
sudo apt-get update
sudo apt-get -y upgrade

#install some deps
sudo apt-get -y install git vlc-nox cmake libopencv-dev incron python-pip python-dev

cd ~

#build and install ffmpeg
git clone https://github.com/FFmpeg/FFmpeg.git
mv FFmpeg ffmpeg
cd ffmpeg
./configure
make -j5
sudo make install
cd ~

#pull the modect userland and build the binary
git clone https://github.com/sodnpoo/userland.git
cd userland
git checkout raspividcv
mkdir build
cd build
cmake ../
make -j5 opencv_modect
cd ~

# link in the default mask
ln -s ~/opencv_modect_tools/mask.png ~

# make the drop directory
mkdir ~/drop

# setup modect to run at boot
echo "@reboot pi /home/pi/opencv_modect_tools/start.sh" | sudo tee -a /etc/cron.d/start_opencv_modect > /dev/null

# sweep up any lost videos
echo "0 */6 * * * pi /home/pi/opencv_modect_tools/sweep.sh" | sudo tee -a /etc/cron.d/start_opencv_modect > /dev/null

## install youtube uploader
#sudo pip install --upgrade google-api-python-client progressbar2
#git clone https://github.com/tokland/youtube-upload.git
#cd youtube-upload/
#sudo python setup.py install
#echo *** dont forget to get /home/pi/client_secrets.json from google ***

#install boto
sudo pip install boto
echo dont forget to configure ~/.aws/credentials

# incrond
echo pi | sudo tee -a /etc/incron.allow > /dev/null
#echo "/home/pi/drop/ IN_MOVED_TO /home/pi/opencv_modect_tools/tsdotyoutube.py \$@/\$#" | sudo tee -a /var/spool/incron/pi
echo "/home/pi/drop/ IN_MOVED_TO /home/pi/opencv_modect_tools/tsdots3.py \$@/\$#" | sudo tee -a /var/spool/incron/pi
sudo chown pi.incron /var/spool/incron/pi
sudo chmod 600 /var/spool/incron/pi

# set correct timezone
sudo ln -fs /usr/share/zoneinfo/Europe/London /etc/localtime
