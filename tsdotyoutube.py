#!/usr/bin/env python
'''
first arg is the full path to a file to be uploaded to youtube

the basename will be a unix timestamp
we need to:

1: extract the date part; this is the playlist
2: extract the time this is the title
'''
from os import path
from datetime import datetime
from youtube_wrapper import youtube_upload
import sys
import socket

tag = socket.gethostname()
client_secrets = "/home/pi/client_secrets.json"

#fn = '/home/pi/drop//1452436732.mp4'
try:
    fn = sys.argv[1]
except:
    print "no filename?"
    sys.exit(1)

bn = path.basename(fn)
en = path.splitext(bn)[0]

print fn, bn, en

unixts = int(en)
dt = datetime.fromtimestamp(unixts)
print dt, dt.date(), dt.time()

title = str(dt.time())
playlist = "%s %s" % (tag, str(dt.date()))
youtube_upload(fn, title, playlist=playlist, privacy='private', delete=True, client_secrets=client_secrets)
