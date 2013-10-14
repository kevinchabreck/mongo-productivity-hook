#!/usr/bin/env python

import subprocess
from datetime import datetime

p = subprocess.Popen(["tail", "-1", "../logs/HEAD"], stdout=subprocess.PIPE)
out, err = p.communicate()
hash = out.split(' ')[1]
timestamp = out.split('> ')[1].split(' ')[0]

print "hash of most recent commit: " + hash
print "timestamp: '{}'".format(timestamp)
print "time: {}".format(datetime.fromtimestamp(float(timestamp)))

p = subprocess.Popen(["git", "diff-tree", "--numstat", hash], stdout=subprocess.PIPE)
out, err = p.communicate()

print "numstat for commit {}:".format(hash)
print out.replace('\n', ' ').replace('\t', ' ').split(' ')

#1381295858