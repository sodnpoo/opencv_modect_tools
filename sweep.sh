#!/bin/bash
for i in $( ls /home/pi/drop ); do /home/pi/opencv_modect_tools/tsdotyoutube.py /home/pi/drop/$i ; done
