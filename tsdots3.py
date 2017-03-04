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
import sys
import socket
import boto
from boto.s3.key import Key
import os

tag = socket.gethostname()

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

#https://github.com/boto/boto/issues/2207
def get_bucket(bucket_name):
  conn = boto.connect_s3()
  bucket = conn.get_bucket(bucket_name)
  bucket_location = bucket.get_location()
  if bucket_location:
    print "bucket_location:", bucket_location
    conn = boto.s3.connect_to_region(bucket_location)
    bucket = conn.get_bucket(bucket_name)
  return bucket


b = get_bucket('sodnpoo-cams')
k = Key(b)
k.key = "%s/%s/%s" % (tag, dt.date().isoformat(), bn)
print "key:", k.key
k.set_contents_from_filename(fn)

#hopefully any exceptions before here will stop us deleting the source file
os.remove(fn)
