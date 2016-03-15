import argparse
import hashlib
import os
import os.path


def dump_folder(atDir, astrOutput, uiIndent):
	strIndent = ' ' * uiIndent
	uiLastItem = len(atDir)-1
	uiCnt = 0

	# Loop over all entries in this folder.
	for strName,tValue in atDir.iteritems():
		if uiCnt==uiLastItem:
			strEnd = ''
		else:
			strEnd = ','

		# If the value is a string this is a file.
		if isinstance(tValue, basestring):
			astrOutput.append('%s[\'%s\']=\'%s\'%s' % (strIndent,strName,tValue,strEnd))
		else:
			astrOutput.append(strIndent + '%s={'%strName)
			dump_folder(tValue, astrOutput, uiIndent+2)
			astrOutput.append(strIndent + '}%s'%strEnd)

		uiCnt += 1



tParser = argparse.ArgumentParser(description='create_luarocks_manifest')
tParser.add_argument(                         dest='strPath', help='Scan PATH for files.', metavar='PATH')
tParser.add_argument(                         dest='tOutputFile', type=argparse.FileType('wt'), help='Write output to FILE.', metavar='FILE')
tParser.add_argument('-v', '--verbose',       dest='fVerbose', action='store_const', const=True, help='Be verbose')
aOptions = tParser.parse_args()

if aOptions.fVerbose==True:
	print 'Rock folder: "%s"' % aOptions.strPath
	print 'Output file: "%s"' % aOptions.tOutputFile.name


# Find files recursively starting at PATH.
if os.path.exists(aOptions.strPath)==False:
	raise Exception('The path "%s" does not exist!' % aOptions.strPath)

if os.path.isdir(aOptions.strPath)==False:
	raise Exception('"%s" is no directory!' % aOptions.strPath)

atResults = {}
for strRoot, astrDirs, astrFiles in os.walk(aOptions.strPath, topdown=True, onerror=None, followlinks=False):
	# Get the relative path from the start to the current folder.
	if os.path.samefile(strRoot, aOptions.strPath)==True:
		strRelPath = ''
	else:
		strRelPath = os.path.relpath(strRoot, aOptions.strPath)

	if len(astrFiles)>0:
		# Get all path components.
		astrAllPathComponents = []
		strPathLeft = strRelPath
		while len(strPathLeft)>0:
			strHead,strTail = os.path.split(strPathLeft)
			if len(strHead)==0:
				astrAllPathComponents.insert(0, strTail)
				strPathLeft = ''
			elif len(strTail)==0:
				astrAllPathComponents.insert(0, strHead)
				strPathLeft = ''
			else:
				astrAllPathComponents.insert(0, strTail)
				strPathLeft = strHead

		atDir = atResults
		for strPathComponent in astrAllPathComponents:
			if not strPathComponent in atDir:
				atDir[strPathComponent] = {}
			atDir = atDir[strPathComponent]

		# Loop over all files and generate the MD5 sum.
		for strFile in astrFiles:
			strFullPath = os.path.join(strRoot, strFile)
			if os.path.samefile(strFullPath, aOptions.tOutputFile.name)==True:
				if aOptions.fVerbose==True:
					print 'Ignoring output file "%s"...' % strFullPath
			else:
				if aOptions.fVerbose==True:
					print 'Processing file "%s"...' % strFullPath
				tFile = open(strFullPath, 'rb')
				tMd5 = hashlib.md5()
				while True:
					strFileData = tFile.read(4096)
					if len(strFileData)>0:
						tMd5.update(strFileData)
						if len(strFileData)<4096:
							break
				atDir[strFile] = tMd5.hexdigest()

# Generate the manifest.
astrManifest = []
astrManifest.append('rock_manifest = {')
dump_folder(atResults, astrManifest, 2)
astrManifest.append('}')

aOptions.tOutputFile.write('\n'.join(astrManifest))
aOptions.tOutputFile.close()

