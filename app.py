import glob, os, zipfile, tarfile

### FUNCTIONS

def extract_tar(tar_file_name, output_dir):
	tar = tarfile.open(tar_file_name, "r:gz")
	tar.extractall(output_dir)
	tar.close()
	return

def extract_zip(zip_file_name, output_dir):
	with zipfile.Zipfile(zip_file_name,"r") as zip_file:
		zip_file.extractall(output_dir)
	return

### END OF FUNCTIONS
takeout_dir = input("Please input the path to your Google Takeout archive: ")
for filename in glob.glob(os.path.join(takeout_dir, 'takeout-*')):
	if (filename.endswith("tgz")):
		extract_tar(filename, takeout_dir)
	elif (filename.endswith("zip")):
		extract_zip(filename, takeout_dir)