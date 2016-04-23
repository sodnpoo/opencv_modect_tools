#!/bin/bash
FPS=15
ROTATION=0
WIDTH=1920
HEIGHT=1080
/home/pi/userland/build/bin/opencv_modect -r $ROTATION -f $FPS -w $WIDTH -h $HEIGHT 2> /dev/null | /home/pi/ffmpeg/ffmpeg -ar 8000 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -thread_queue_size 512 -f h264 -r $FPS -i - -vcodec copy -acodec aac -ab 64k -g 30 -strict experimental -f mpegts -r $FPS pipe:1 2>/dev/null | python /home/pi/opencv_modect_tools/snapcat.py &
