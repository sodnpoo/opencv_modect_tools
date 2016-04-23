#!/usr/bin/python

'''
something like:

1. read from stdin as fast as we can
2. on USR1 start writing to a file
3. on USR2 stop writing


 ffmpeg -i 'udp://127.0.0.1:2000?buffer_size=2000000&fifo_size=100000' -vcodec copy -acodec copy -g 30 -f mpegts "pipe:1" | python snapcat.py

 ./opencv_modect | ~/ffmpeg/ffmpeg -ar 8000 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i  /dev/zero -thread_queue_size 512 -f h264 -i - -vcodec copy -acodec aac -ab 64k -g 30 -strict  experimental -f mpegts pipe:1 | python ~/snapcat.py

'''

TMPDIR = "/tmp/"
DROPDIR = "/home/pi/drop/"

BLOCKSIZE = 1024
MAXBLOCKS = 1024

import sys
import time
import signal
import os
import collections

blockbuffer = collections.deque(maxlen=MAXBLOCKS)
outf = None
outfn = None

def stop():
    print "stop"
    global outf, outfn
    #outf.close()
    outf = None

    fn = "%s/%s" % (TMPDIR, outfn)
    dropfn = "%s/%s" % (DROPDIR, outfn)
    try:
      os.rename(fn, dropfn)
    except:
      pass
    outfn = None

def start():
    print "start"
    global outf, outfn
    if outf is not None:
        print "already started?"
        return

    ts = int(time.time())
    outfn = "%s.mp4" % ts
    fn = "%s/%s" % (TMPDIR, outfn)
    print "fn:",fn
    outf = open(fn, "wb")

def maybe_write(buf):
    #print buf

    if outf is None:
        return

    outf.write(buf)

def maybe_write_buffer(buf):
    #print buf
    blockbuffer.append(buf)

    if outf is None:
        return

    b = blockbuffer.popleft()
    try:
      outf.write(b)
    except:
      pass

def usr1_handler(signum, frame):
    #print "usr1_handler:", signum
    start()

def usr2_handler(signum, frame):
    #print "usr2_handler:", signum
    stop()

signal.signal(signal.SIGUSR1, usr1_handler)
signal.signal(signal.SIGUSR2, usr2_handler)

while True:
    b = sys.stdin.read(BLOCKSIZE)

    maybe_write_buffer(b)
    #maybe_write(b)
