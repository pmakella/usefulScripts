import subprocess
import sys
import re
import glob

import os.path
# gives new file names used in IDR pipeline for old file names with BIDs
fileobj = open(sys.argv[1],"r")
info = fileobj.readlines()
# worm pipeline
lines = info
newnames = []
datafiles = []
for i in xrange(len(lines)):
        s=lines[i].strip()
        sl=s.split('\t')
	if (len(sl) != 17):
		print 'invalid ce config file, line ' + str(i) + '\n'
	else:
		datafiles.append(sl[16])
		factor = sl[1] + '_' + sl[6] + '_' + sl[4]
		source = sl[9]
		replicate = sl[8]
		abid = sl[10]
		name = factor+'_'+source+'_'+abid+'_Rep'+replicate
	        newnames.append(name)




print 'datafiles with bids -->  new names\n'

for i in xrange(len(datafiles)):
	print datafiles[i] + ' --> '+ newnames[i]
