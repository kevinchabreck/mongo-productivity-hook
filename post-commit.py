#!/usr/bin/env python

import subprocess, pymongo, math
from datetime import datetime

# fetch the hash and the timestamp from the most recent commit
p = subprocess.Popen(["tail", "-1", ".git/logs/HEAD"], stdout=subprocess.PIPE)
out, err = p.communicate()
hash = out.split(' ')[1]
timestamp = out.split('> ')[1].split(' ')[0]
time = datetime.fromtimestamp(float(timestamp)) #create datetime object

# pull insertions, deletions, and # of files edited from the numstat of the commit
p = subprocess.Popen(["git", "diff-tree", "--numstat", hash], stdout=subprocess.PIPE)
out, err = p.communicate()
insertions = deletions = 0
lines = out.split('\n')
for i in range(1, len(lines) - 1):
	line = lines[i].split('\t')
	insertions += int(line[0])
	deletions += int(line[1])
files = len(lines) - 2

# get the hash of each blob in the most recent two commits 
# sum the size difference from each blob pair to get the total size of the most recent commit
p = subprocess.Popen(["git", "diff-tree", hash], stdout=subprocess.PIPE)
out, err = p.communicate()
size = 0
lines = out.split('\n')
for i in range(1, len(lines) - 1):
	line = lines[i].split(' ')
	if int(line[2], 16) == 0:
		sizeA = 0
	else:
		p = subprocess.Popen(["git", "cat-file", "-s", line[2]], stdout=subprocess.PIPE)
		sizeA, err = p.communicate()
	if int(line[3], 16) == 0:
		sizeB = 0
	else:
		p = subprocess.Popen(["git", "cat-file", "-s", line[3]], stdout=subprocess.PIPE)
		sizeB, err = p.communicate()
	#use the absolute value of the difference (in case code has been removed)
	size += math.fabs(int(sizeB) - int(sizeA))

# build the dictionary of commit metadata to be stored in the database
commit = { 	"hash": hash,
			"day": time.weekday(),
			"hour": time.hour,
			"insertions": insertions,
			"deletions": deletions,
			"files": files,
			"size": size }

# store the "commit" document in a mongo database
mongourl = 'mongodb://localhost:27017/' #replace with the url of the centralized db
client = pymongo.MongoClient(mongourl)
db = client.commitdb #replace 'commitdb' with the name of the centralized db
collection = db.commits #replace 'commits' with the name of a collection in the centralized db
collection.insert(commit)

print commit