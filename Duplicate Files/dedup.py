from sys import argv
import hashlib
import os

#It creates a map with key as Hash Value and the value as list of files having same hash(= key)
def createmap(hash_vs_path,root):
	for subdir, dirs, files in os.walk(root):
		for file in files:
			filepath = os.path.join(subdir,file)
			key = hashlib.md5(open(filepath,'rb').read()).hexdigest()
			if key not in hash_vs_path:
				hash_vs_path[key] = [filepath]
			else:
				hash_vs_path[key].append(filepath)

#This functions list the duplicate files so that user can select the ones to delete
def printduplicate(hash_vs_path):
	i = 1
	dupdict = dict()
	for key in hash_vs_path:
		if len(hash_vs_path[key]) > 1:
			print str(i)+") "+"Duplicate files with path are : "
			print ', '.join(hash_vs_path[key])
			print "-"*70
			dupdict[i] = str(key)
			i += 1
	return dupdict

#This functions accepts the name of the file to keep and delete its duplicates
def dedup(dupdict,hash_vs_path):
	index = input("Enter the index for deduplication(0 to exit) : ")
	while True:
		if index > 0 and index <= len(dupdict) and index in dupdict:
			break
		if index == 0:
			exit(0)
		else:
			index = input("Please enter valid index : ") 
	hashkey = dupdict[index]
	file_to_keep = raw_input("Enter the file name to keep(Along with path) : ")
	while True:
		if file_to_keep in hash_vs_path[hashkey]:
			break
		else:
			file_to_keep = raw_input("Enter the valid file name to keep(Along with path) : ")
	del dupdict[index]
	for duplicate_file in hash_vs_path[hashkey]:
		if duplicate_file != file_to_keep:
			os.remove(duplicate_file)
	return file_to_keep

def main(argv):
	try:
		root = str(argv[1])
	except:
		print "usage: python dedup.py <path>"
		exit(0)
	if not os.path.exists(root):
		print "No such path exists"
	else:
		hash_vs_path = dict()
		createmap(hash_vs_path,root)
		dupdict = printduplicate(hash_vs_path)
		while True:
			if dupdict:
				file_to_keep = dedup(dupdict,hash_vs_path)
				print "Removed Duplicates for",file_to_keep
			else:
				print "No duplicate files in this directory"
				break

if __name__ == "__main__":
	main(argv)