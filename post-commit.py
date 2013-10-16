#!/usr/bin/env python

import subprocess, pymongo
from datetime import datetime

p = subprocess.Popen(["tail", "-1", ".git/logs/HEAD"], stdout=subprocess.PIPE)
out, err = p.communicate()
hash = out.split(' ')[1]
timestamp = out.split('> ')[1].split(' ')[0]

#print "hash of most recent commit: " + hash
#print "timestamp: '{}'".format(timestamp)
print "time: {}".format(datetime.fromtimestamp(float(timestamp)))

p = subprocess.Popen(["git", "diff-tree", "--numstat", hash], stdout=subprocess.PIPE)
out, err = p.communicate()

print "numstat for commit {}:\n".format(hash)
print out

lines = out.split('\n')
for i in range(1, len(lines) - 1):
	line = lines[i].split('\t')
	insertions = line[0]
	deletions = line[1]
	file = line[2]
	print("file: {} \n{} insertions, {} deletions".format(file, insertions, deletions))

commit = { 	"hash": hash,
			"insertions": insertions,
			"deletions": deletions,
			"timestamp": timestamp }
#print out.replace('\n', ' ').replace('\t', ' ').split(' ')