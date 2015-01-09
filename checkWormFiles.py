import subprocess
import sys
import re
import glob
from collections import defaultdict
import os.path

# checks if output files from IDR pipeline exist in current directory

fileobj = open(sys.argv[1],"r")
info = fileobj.readlines()

#dictionary to store (key, values), key= dataset name, values = list of inputs, IPs 
d = defaultdict(list)
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
		
		d[factor].append(source+'_Rep'+replicate)
                name = factor+'_'+source+'_Rep'+replicate
                newnames.append(name)


print 'datafiles with bids -->  new names\n'
dirname = os.getcwd()

for i in xrange(len(datafiles)):
        print datafiles[i] + ' --> '+ newnames[i]
####################################################################################################
# remove duplicate entries in Rep column, they would concatenated in download_xxx.sh
#print d
for key in d:
	print key
	print d[key]
	#ll=list(set:w(d[key][0]))
	d[key]=list(set(d[key]))
	#d[key][0] = ll
#print 'here' 
#print d
# add pooled Inputs and IPs to dictionary
for i in d.iteritems():
	src=[]
	rep=[]
	# to find if inputs/IPs are more than 1
	for j in xrange(len(i[1])):
		s=i[1][j].split('_')
		src.append(s[0])
		rep.append(s[1])
	
	while (len(src)>0):
		elem=src[0]
		if (src.count(elem)>1):
			#add to d
			if (elem == 'Input'):
				d[i[0]].append(elem+'_Rep0')
			else:
				d[i[0]].append('IP'+'_Rep0')
			#delete these items
			src = [x for x in src if x != elem]
		else:
			# delete processed element
			src = [x for x in src if x != elem]
		
print d

####################################################################################################
print 'checking for output files in current working directory' + str(dirname)
print 'checking q30.sam files...'
numfound = 0
# each of the files in newnames should have a q30.sam
for n in newnames:
	file_path=dirname+'/'+n+'_q30.sam'
        if(os.path.exists(file_path)==True):
        	numfound = numfound + 1	
        else:
                print file_path , 'does not exist\n'

print '..found ' + str(numfound)+' files.\n'


####################################################################################################
print 'checking tagAlign.gz files...'

# check for  each of the files in d 
for i in d.iteritems():
	print 'dataset ' + str(i[0])
	numfound = 0
	for j in xrange(len(i[1])):
		fn = str(i[0]) +'_'+ str(i[1][j])
                print fn
                file_path = dirname+'/'+fn+'.tagAlign.gz'
                if(os.path.exists(file_path)==True):
                        numfound = numfound + 1
                else:
                        print file_path , 'does not exist\n'

		# check for pr1 and pr2 files
		if ('Input' not in str(i[1][j])):
			fn = str(i[0]) +'_'+ str(i[1][j]) +'.pr1'
			print fn
			file_path = dirname+'/'+fn+'.tagAlign.gz'
        		if(os.path.exists(file_path)==True):
        			numfound =numfound +1
        		else:
        		        print file_path , 'does not exist\n'

		
			fn = str(i[0]) +'_'+ str(i[1][j]) + '.pr2'
                        print fn
                        file_path = dirname+'/'+fn+'.tagAlign.gz'
                        if(os.path.exists(file_path)==True):
                                numfound = numfound + 1
                        else:
                                print file_path , 'does not exist\n'
	print '..found ' + str(numfound)+' files.\n'


####################################################################################################
print 'checking .bam files...'

for i in d.iteritems():
                files =[]
                file_path=dirname+'/'+str(i[0])+'_Input*.bam'
                files = glob.glob(file_path)
                if(len(files)>=1):
                        print files
                else:
                        print file_path , ' does not exist in current  directory\n'

####################################################################################################
print 'checking .regionPeak.gz files...'

for i in d.iteritems():
	print 'dataset ' + str(i[0])
	numfound =0
	for j in xrange(len(i[1])):

                # check for pr1 and pr2 files as well
                if ('Input' not in str(i[1][j])):

                	files =[]
			fn = str(i[0]) +'_'+ str(i[1][j])
	                file_path = dirname+'/'+fn+'.tagAlign*.regionPeak.gz'
			print file_path
        	        files = glob.glob(file_path)
			if(len(files)==1):
                	        numfound = numfound+1
                	else:
                        	print file_path , 'does not exist\n'

                        files=[]
			fn = str(i[0]) +'_'+ str(i[1][j]) +'.pr1'
	                file_path = dirname+'/'+fn+'.tagAlign*.regionPeak.gz'
        	        print file_path
			files = glob.glob(file_path)
			if(len(files)==1):
                                numfound =numfound +1
                        else:
                                print file_path , 'does not exist\n'


                        fn = str(i[0]) +'_'+ str(i[1][j]) + '.pr2'
	                file_path = dirname+'/'+fn+'.tagAlign*.regionPeak.gz'
        	        print file_path
			files = glob.glob(file_path)
			if(len(files)==1):
                                numfound = numfound +1
                        else:
                                print file_path , 'does not exist\n'

	print '..found ' + str(numfound)+' files.\n'


####################################################################################################

print 'checking for .txt files...'

for i in d.iteritems():
        print 'dataset ' + str(i[0])
        numfound =0
        for j in xrange(len(i[1])):

                # check for pr1 and pr2 files as well
                if ('Input' not in str(i[1][j])):

                        files =[]
                        fn = str(i[0]) +'_'+ str(i[1][j])
                        file_path = dirname+'/'+fn+'.pr1*' + fn+'.pr2*.txt'
                        print file_path
                        files = glob.glob(file_path)
                        if(len(files)==3):
                                numfound = numfound+3
                        else:
                                print file_path , '3 files do not exist\n'


	#list of Replicates
	list1 =i[1]
	replist = [x for x in list1 if 'IP' not in x and 'Input' not in x]
	print replist	

	while (len(replist)>1):

        	files=[]
                fn = str(i[0]) +'_'+ replist[0] +'*'+ replist[1]+'*.txt'
                fn1 = str(i[0]) +'_'+ replist[1] +'*'+ replist[0]+'*.txt'
                file_path = dirname+'/'+fn
                file_path1 = dirname+'/'+fn1
                print file_path + 'or' + file_path1
                files = glob.glob(file_path)
                files1 = glob.glob(file_path1)
                if(len(files)==3 or len(files1)==3):
                        numfound =numfound +3
                else:
                        print '3 files do not exist for both '+ file_path +'and'+ file_path1+ '\n'
		#remove first item in list
		replist.remove(replist[0])

	print '..found ' + str(numfound)+' files.\n'
