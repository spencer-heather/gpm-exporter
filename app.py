import glob, os, zipfile, tarfile

### BEGINNING OF FUNCTIONS

def extract_tar(tar_file_name, output_dir):
	with tarfile.open(tar_file_name,"r:gz") as tar_file:
		tar_file.extractall(output_dir)
	return

def extract_zip(zip_file_name, output_dir):
	with zipfile.Zipfile(zip_file_name,"r") as zip_file:
		zip_file.extractall(output_dir)
	return

### END OF FUNCTIONS
### BEGINNING OF APP
takeout_dir = input("Please input the path to your Google Takeout archive: ")
for filename in glob.glob(os.path.join(takeout_dir, 'takeout-*')):
	if (filename.endswith("tgz")):
		extract_tar(filename, takeout_dir)
	elif (filename.endswith("zip")):
		extract_zip(filename, takeout_dir)
### END OF APP