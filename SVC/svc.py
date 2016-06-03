'''

Simple Version Control
	The base directory .svc contains two files
	-changes
	-latest_version
	The 'changes' file keeps track of the changes made, this file is modified after every valid commit.
	The 'latest_version' file maintains the latest version of the file.

'''

from sys import argv
import os

COMMIT_APPEND_LINE = 0
COMMIT_DELETE_LINE = 1
COMMIT_ERROR = 2

def validate_commit(file_name,latest_version_path):
	try:
		file_data = open(file_name,'r').read().split("\n")
	except:
		print "No such file exists"
		exit(0)
	latest_version_data = open(latest_version_path,'r').read().split()
	if file_data == latest_version_data:
		print "No changes"
		return (3,)
	if (len(file_data)-len(latest_version_data)) == 1: #Added onle line to the end of file
		if file_data[:-1] != latest_version_data:
			return (COMMIT_ERROR,)
		return (COMMIT_APPEND_LINE,)
	elif (len(latest_version_data)-len(file_data)) == 1: #One line deleted
		file_data_index = 0
		latest_version_data_index = 0
		difference = 0
		while file_data_index < len(file_data):
			if file_data[file_data_index] == latest_version_data[latest_version_data_index]:
				file_data_index += 1
				latest_version_data_index += 1
			else:
				difference += 1
				if difference > 1:
					break
				deleted_line = latest_version_data[latest_version_data_index]
				deleted_line_index = latest_version_data_index
				latest_version_data_index += 1
		if difference == 0 and file_data_index == len(file_data):
			deleted_line_index = file_data_index 
			deleted_line = latest_version_data[deleted_line_index]
			difference = 1
		if difference != 1:
			return (COMMIT_ERROR,)
		else:
			return (COMMIT_DELETE_LINE,deleted_line_index,deleted_line,)
	else:
		return (COMMIT_ERROR,)

def print_version(commit_id):
	latest_version_path = ".svc/latest_version"
	changes_path = ".svc/changes"
	try:
		changes_data = open(changes_path,'r').read().split("\n")[:-1]
	except:
		changes_data = open(changes_path,'w')
		changes_data.close()
		changes_data = open(changes_path,'r').read().split("\n")[:-1]
	if commit_id < 0 or commit_id > len(changes_data):
		print "Invalid commit id"
		return
	current_data = open(latest_version_path,'r').read().split("\n")
	for i in range(len(changes_data)-1,commit_id-1,-1):
		change = changes_data[i].split()
		if change[0] == '+':
			current_data = current_data[:-1]
		else:
			deleted_line_index = int(change[1])
			deleted_line = change[2]
			current_data = current_data[:deleted_line_index] + [deleted_line] + current_data[deleted_line_index:]
	print '\n'.join(current_data)

def main(argv):
	if len(argv) != 2:
		print "usage: svc <file_name> or svc <commit_id>"
		return 
	try:
		commit_id = int(argv[1])
		try:
			print_version(commit_id)
		except:
			print "Error"
	except:
		directory  = ".svc"
		if not os.path.exists(directory):
			os.makedirs(directory)
		file_name = argv[1]
		latest_version_path = ".svc/latest_version"
		changes_path = ".svc/changes"
		if not os.path.isfile(latest_version_path):
			latest_version = open(latest_version_path,'w')
			latest_version.write(open(file_name,'r').read())
			latest_version.close()
			print "Initial commit successfull"
		else:
			commit = validate_commit(file_name,latest_version_path)
			if commit[0] == COMMIT_APPEND_LINE:
				latest_version = open(latest_version_path,'w')
				latest_version.write(open(file_name,'r').read())
				latest_version.close()
				changes = open(changes_path,'a')
				changes.write("+\n")
				changes.close()
				print "Commit Successfull. Commit ID : ",len(open(changes_path,'r').read().split("\n"))-1
			elif commit[0] == COMMIT_DELETE_LINE:
				latest_version = open(latest_version_path,'w')
				latest_version.write(open(file_name,'r').read())
				latest_version.close()
				changes = open(changes_path,'a')
				changes.write("- "+str(commit[1])+" "+commit[2]+"\n")
				changes.close()
				print "Commit Successfull. Commit ID : ",len(open(changes_path,'r').read().split("\n"))-1				
			elif commit[0] == COMMIT_ERROR:
				print "Commit Error"

if __name__ == "__main__":
	main(argv)