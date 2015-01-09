import fnmatch
import os
import sys

# deletes files and their hard links on XRaid

fileobj = open(sys.argv[1],"r")
files = fileobj.readlines()

#project name
prjname =sys.argv[2]

for i, val in enumerate(files):
        files[i] = val.strip()

print files

matches = []

for root, dirnames, filenames in os.walk("/XRaid"):
    for i in files:
        for filename in fnmatch.filter(filenames, i):
            matches.append(os.path.join(root, filename))

if len(matches) > 0:
	outfile = open(prjname+'.log', 'w')
	outfile.write("File deleted in project :" + prjname)
	outfile.write("\n".join(matches))
	outfile.write("\n")
	outfile.close()
	print matches
	for item in matches:
		os.remove(item)

	print 'Files deleted in project : '+ prjname
	print 'log file written: ' + prjname + '.log'

else:
	print 'no files to delete'
