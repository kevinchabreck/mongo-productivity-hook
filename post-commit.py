#!/usr/bin/env python

import subprocess, pymongo, math
from datetime import datetime

# fetch the hash and the timestamp from the most recent commit
p = subprocess.Popen(["tail", "-1", ".git/logs/HEAD"], stdout=subprocess.PIPE)
out, err = p.communicate()
hash = out.split(' ')[1]
timestamp = out.split('> ')[1].split(' ')[0]
time = datetime.fromtimestamp(float(timestamp))

# pull insertions, deletions, and # of files edited from the numstat of the commit
p = subprocess.Popen(["git", "diff-tree", "--numstat", hash], stdout=subprocess.PIPE)
out, err = p.communicate()
insertions = deletions = 0
lines = out.split('\n')
for i in range(1, len(lines) - 1):
	line = lines[i].split('\t')
	insertions += int(line[0])
	deletions += int(line[1])

# get the file size in bytes of each blob in the most recent two commits, and take 
# the difference to get the "size" of the commit
p = subprocess.Popen(["git", "diff-tree", hash], stdout=subprocess.PIPE)
out, err = p.communicate()
size = 0
lines = out.split('\n')
for i in range(1, len(lines) - 1):
	line = lines[i].split(' ')
	p = subprocess.Popen(["git", "cat-file", "-s", line[2]], stdout=subprocess.PIPE)
	sizeA, err = p.communicate()
	p = subprocess.Popen(["git", "cat-file", "-s", line[3]], stdout=subprocess.PIPE)
	sizeB, err = p.communicate()
	size += math.fabs(int(sizeB) - int(sizeA))

# build the dictionary to be stored in the database
commit = { 	"hash": hash,
			"timestamp": timestamp,
			"day": time.weekday(),
			"hour": time.hour,
			"insertions": insertions,
			"deletions": deletions,
			"files": len(lines) - 1,
			"size": size }

# store the document in a mongo database

print commit