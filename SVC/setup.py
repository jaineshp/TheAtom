from distutils.core import setup

files = ["README.md", "svc.py"]

setup(
	name 			 = "svc",
	version 		 = "1.0",
	description 	 = "Simple Version Control",
	packages 		 = ['.'],
	package_data 	 = { 'package' : files },
	scripts 		 = ["bin/svc"],
	long_description = "usage: svc <file_name> or svc <commit_id>"
) 