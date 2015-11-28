#!/usr/bin/env python
#coding=-utf-8

import os
import sys
import glob

path = ''

if len(sys.argv) < 2:
    print 'usage: count.py [path]'    
    sys.exit(1)
else:
    path = os.path.abspath(sys.argv[1])

files = glob.glob(os.path.join(path, '*'))

objects = set()

for fname in files:
    parts = fname.split('_')
    prj_id = parts[1]
    objects.add(prj_id)

print len(objects)
for obj in objects:
    print obj
