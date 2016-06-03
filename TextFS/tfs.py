'''
TextFS :

The following structure in maintained in the file '.tfs' which is located in the home directory 

Base File Structure - 
	Super Block Structure
		0	FileSystem Name
		1	Inode count					100
		2	Blocks count				100000
		3	Free inodes
		4	Inode Map Columns(Count)	3
		5	Inode size(in lines)		5
		6	Block size(in lines)		5
		7	Inode Map Start				13
		8	Block Start					614
		9   Last Access Time
		10  Last Modified Time
		11  Number of blocks in file

	File Name to Inode Map
		This will contain 3 columns namely - Exists/Deleted, File Name, Inode number

	Inode entries(100 * INODE_SIZE)

	Inode Structure - 
		0	Number of Lines
		1	Last Read Time
		2	Creation Time
		3	List of Data Blocks(Space separated)
		4	Write Time

	List of free data blocks(Space separated)

	Data blocks

'''

from time import gmtime, strftime
from sys import argv
import os

usage = "usage: tfs {create|copy|echo|delete|ls}"

time_stamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())

commands = {
	"create" : 1,
	"copy"	 : 2,
	"echo"	 : 3,
	"delete" : 4,
	"ls"	 : 5,
}

MAX_INODES 			= 100
FREE_INODES			= 100
INODE_SIZE 			= 5
BLOCK_SIZE 			= 5
MAP_START 			= 13
BLOCK_START 		= 614
INODE_ENTRIES_START = 113
FREE_DATA 			= 613

BASE_FILE = os.environ['HOME']+"/.tfs"

#This function writes the data list into the file file_name
def write(file_name,data):
	with open(file_name,'w') as f:
		for d in range(len(data)):
			if d != len(data)-1:
				f.write(str(data[d])+'\n')
			else:
				f.write(str(data[d]))

#This function is used to create the base file .tfs, this will the hidden file and stored in the home directory
def create_base_file():
	initial = ["TextFS",100,100000,100,3,5,5,13,614,-1,-1,0]
	for i in range(1,101):
		initial.append("0 "+str(i))
	for i in range(100):
		for j in range(5):
			initial.append(0)
	initial.append(0)
	write(BASE_FILE,initial)

#This is used to get the FS details
def get_superblock():
	data = open(BASE_FILE,'r').read().split("\n")
	data = data[1:9]
	data = [0] + data
	data = map(int,data)
	MAX_INODES 	= data[1]
	FREE_INODES = data[3]
	INODE_SIZE 	= data[5]
	BLOCK_SIZE  = data[6]
	MAP_START 	= data[7]
	BLOCK_START = data[8] 

#This is used to create the file
def create(file_name):
	get_superblock();
	data = open(BASE_FILE,'r').read().split("\n")
	data = [0] + data
	if FREE_INODES == 0:
		print "No more space"
		return
	file_names = []
	for i in range(MAP_START,MAP_START+MAX_INODES):
		current = data[i].split()
		if int(current[0]) == 1:
			file_names.append(current[2])
	if file_name in file_names:
		print "File with same name already exists"
		return
	for i in range(MAP_START,MAP_START+MAX_INODES):
		current = data[i].split()
		if int(current[0]) == 0:
			break
	fs_index = i
	inode_no = int(current[1])
	data[fs_index] = "1 "+str(inode_no)+" "+str(file_name)
	inode_start = INODE_ENTRIES_START + (inode_no-1)*INODE_SIZE
	data[inode_start+2] = time_stamp
	data[10] = time_stamp #Timestamps of the Superblock will be updated
	data[11] = time_stamp
	data[4] = int(data[4]) - 1 #Inode count is decremented
	write(BASE_FILE,data[1:])
	print "File",file_name,"created"

#This is used to display the list of files in the TextFS
def ls():
	data = open(BASE_FILE,'r').read().split("\n")
	data = [0] + data
	data[10] = time_stamp
	file_names = []
	for i in range(MAP_START,MAP_START+MAX_INODES):
		if data[i][0] == "1":
			file_names.append(data[i].split()[2])
	if len(file_names):
		print '\n'.join(file_names)

#This is used to delete the file, here only entries of Inode are cleared and not the data
def delete(file_name):
	data = open(BASE_FILE,'r').read().split("\n")
	data = [0] + data
	got = False
	for i in range(MAP_START,MAP_START+MAX_INODES):
		if data[i][0] == "1" and data[i].split()[2] == file_name:
			got = True
			break
	if not got:
		print "No such file exists"
		return
	data[10] = time_stamp
	data[11] = time_stamp
	current = data[i].split()
	fs_index = i
	inode_no = int(current[1])
	data[i] = "0 "+str(inode_no)
	inode_start = INODE_ENTRIES_START + (inode_no-1)*INODE_SIZE
	data_blocks = map(int,data[inode_start+3].split())
	already = map(int,data[FREE_DATA].split())
	if len(data_blocks) and data_blocks[0] != 0:
		if len(already) and already[0] != 0:
			already.extend(data_blocks)
		else:
			already = data_blocks[:]
		data[FREE_DATA] = ' '.join(map(str,already)) #list of data blocks is appended to free data blocks list
	for i in range(5):
		data[inode_start+i] = 0
	data[4] = int(data[4]) + 1
	write(BASE_FILE,data[1:])
	print "File deleted"

#This is used to copy contents from external file to the file in TextFS
def copy(src_file,destn_file):
	src_data = open(src_file,'r').read().split('\n')
	data = open(BASE_FILE,'r').read().split("\n")
	data = [0] + data
	blocks_in_file = int(data[12])
	got = False
	for i in range(MAP_START,MAP_START+MAX_INODES):
		if data[i][0] == "1" and data[i].split()[2] == destn_file:
			got = True
			break
	if not got:
		print "No such file exists, first create the file using create command"
		return
	current = data[i].split()
	fs_index = i
	inode_no = int(current[1])
	inode_start = INODE_ENTRIES_START + (inode_no-1)*INODE_SIZE
	data_blocks = map(int,data[inode_start+3].split())
	if data_blocks[0] == 0:
		data_blocks = []
	else:
		print "File cannot be overwritten"
		return
	free_data_blocks = map(int,data[FREE_DATA].split())
	lines_to_copy = len(src_data)
	data[inode_start] = lines_to_copy
	data[inode_start+1] = time_stamp
	free_ptr = 0
	i = 0
	to_remove_free = []
	if len(free_data_blocks) and free_data_blocks[0] != 0: #Check if any free data blocks exists
		while i < lines_to_copy and free_ptr < len(free_data_blocks):
			block_id = free_data_blocks[free_ptr]
			fs_id = BLOCK_START + (block_id-1)*BLOCK_SIZE
			written = 0
			data_blocks.append(block_id)
			to_remove_free.append(block_id)
			while i < lines_to_copy and written < BLOCK_SIZE:
				data[fs_id+written] = src_data[i]
				written += 1
				i += 1
			free_ptr += 1
	for j in to_remove_free: #Remove the blocks used from free data blocks list
		free_data_blocks.remove(j)
	while i < lines_to_copy: #Increase the file size if required
		new_block_id = blocks_in_file + 1
		data.extend([0]*5)
		blocks_in_file += 1
		fs_id = BLOCK_START + (new_block_id-1)*BLOCK_SIZE
		written = 0
		data_blocks.append(new_block_id)
		while i < lines_to_copy and written < BLOCK_SIZE:
			data[fs_id+written] = src_data[i]
			written += 1
			i += 1
	data[10] = time_stamp
	data[11] = time_stamp
	data[12] = blocks_in_file
	data[inode_start+3] = ' '.join(map(str,data_blocks))
	data[FREE_DATA] = ' '.join(map(str,free_data_blocks))
	write(BASE_FILE,data[1:])
	print "Contents copied"

#This is used to display the contents of the file in TextFS
def echo(file_name):
	data = open(BASE_FILE,'r').read().split("\n")
	data = [0] + data
	blocks_in_file = int(data[12])
	got = False
	for i in range(MAP_START,MAP_START+MAX_INODES):
		if data[i][0] == "1" and data[i].split()[2] == file_name:
			got = True
			break
	if not got:
		print "No such file exists, first create the file using create command"
		return
	print_data = []
	current = data[i].split()
	fs_index = i
	inode_no = int(current[1])
	inode_start = INODE_ENTRIES_START + (inode_no-1)*INODE_SIZE
	data[inode_start+4] = time_stamp
	data_blocks = map(int,data[inode_start+3].split())
	no_of_lines = int(data[inode_start])
	if no_of_lines == 0:
		return
	i = 0
	while no_of_lines:
		while no_of_lines and i < len(data_blocks):
			block_id = data_blocks[i]
			fs_id = BLOCK_START + (block_id-1)*BLOCK_SIZE
			block_ptr = 0
			while no_of_lines and block_ptr < BLOCK_SIZE:
				print_data.append(data[fs_id+block_ptr])
				block_ptr += 1
				no_of_lines -= 1
			i += 1
	data[10] = time_stamp 
	print '\n'.join(print_data)

def main(argv):
	if not os.path.isfile(BASE_FILE):
		create_base_file()
	if len(argv) < 2 or len(argv) > 4:
		print usage
		return
	command = argv[1]
	if command not in commands:
		print usage
		return
	command_id = commands[command]
	if command_id == 1:
		try:
			file_name = argv[2]
			if (len(argv) != 3):
				print "usage: tfs create <file_name>"
				return
		except:
			print "Please enter file name"
			return
		try:
			create(file_name)
		except:
			print "Error in file creation"
	elif command_id == 2:
		try:
			src_file = argv[3]
			destn_file = argv[2]
			if not os.path.isfile(src_file):
				print "No file named",src_file,"exists"
				return
		except:
			print "usage: tfs copy <destn_file> <src_file>"
			return
		try:
			copy(src_file,destn_file)
		except:
			print "Error in copying contents from",src_data,"to",destn_file
	elif command_id == 3:
		try:
			file_name = argv[2]
		except:
			print "Please enter file name"
			return
		try:
			echo(file_name)
		except:
			print "Error in displaying contents"
	elif command_id == 4:
		try:
			file_name = argv[2]
		except:
			print "Please enter file name"
			return
		try:
			delete(file_name)
		except:
			print "Error in deleting",file_name
	else:
		if len(argv) != 2:
			print usage
			return
		try:
			ls()
		except:
			print "Error in listing files"

if __name__ == "__main__":
	main(argv)