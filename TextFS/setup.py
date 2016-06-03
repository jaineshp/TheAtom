from distutils.core import setup

files = ["README.md", "tfs.py"]

setup(
	name 			 = "tfs",
	version 		 = "1.0",
	description 	 = "TextFS",
	packages 		 = ['.'],
	package_data 	 = { 'package' : files },
	scripts 		 = ["bin/tfs"],
	long_description = "usage: tfs {create|copy|echo|delete|ls}"
) 
