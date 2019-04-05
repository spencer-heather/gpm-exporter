import glob, os, zipfile, tarfile, csv, html, json, argparse, textwrap
from pathlib import Path
from operator import itemgetter

### FUNCTIONS

def extract_tar(tar_file_name, output_dir):
	with tarfile.open(tar_file_name,"r:gz") as tar_file:
		tar_file.extractall(output_dir)
	return

def extract_zip(zip_file_name, output_dir):
	with zipfile.Zipfile(zip_file_name,"r") as zip_file:
		zip_file.extractall(output_dir)
	return

def import_playlists(gpm_playlist_dir):
	playlist_list = []
	for folder in glob.glob(os.path.join(gpm_playlist_dir, '*/')):
		playlist_list.append(folder)
	return playlist_list

def parse_playlist_metadata(metadata_file):
	with open(metadata_file) as metadataCSV:
		csv_data = list(csv.reader(metadataCSV))
		playlist_data = {'title': html.unescape(csv_data[1][0]), 'owner': html.unescape(csv_data[1][1]), 'description': html.unescape(csv_data[1][2]), 'shared': html.unescape(csv_data[1][3]), 'deleted': html.unescape(csv_data[1][4]), 'data': []}
	return playlist_data

def parse_track_data(track_file):
	with open(track_file) as trackfileCSV:
		csv_data = list(csv.reader(trackfileCSV))
		track_data = {'title': html.unescape(csv_data[1][0]), 'album': html.unescape(csv_data[1][1]), 'artist': html.unescape(csv_data[1][2]), 'duration': html.unescape(csv_data[1][3]), 'rating': html.unescape(csv_data[1][4]), 'play_count': html.unescape(csv_data[1][5]), 'removed': html.unescape(csv_data[1][6]), 'playlist_index': html.unescape(csv_data[1][7])}
	return track_data


### VARIABLES

valid_output_formats = ['plex', 'spotify', 'json', 'm3u']


### PARSE ARGUMENTS

parser = argparse.ArgumentParser(description="Parse Google Takeout data", 
	formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-t", "--takeout_dir", type=str, dest="takeout_dir", help="Path to directory containing the Google Takeout archive")
parser.add_argument("-o", "--output", type=str, dest="output",
	help=textwrap.dedent('''\
		Target output type:
		plex
		spotify
		json
		m3u
		'''))
args = parser.parse_args()

takeout_dir = args.takeout_dir
output = args.output


### BEGINNING OF APP

# Get directory to do work in
if (takeout_dir is None):
	takeout_dir = Path(input("Please input the path to your Google Takeout archive: "))
while (output not in valid_output_formats):
	output = input("Specify output format. Valid outputs are:\n{}\n▶ ".format("\n".join(valid_output_formats)))

# Find and extract the Takeout archive
takeout_file = glob.glob(os.path.join(takeout_dir, 'takeout-*'))[0]
if Path(takeout_file).is_file():
	if (takeout_file.endswith("tgz")):
		extract_tar(takeout_file, takeout_dir)
	elif (takeout_file.endswith("zip")):
		extract_zip(takeout_file, takeout_dir)
	else:
		print(takeout_file, "does not appear to be a .tgz or a .zip file.")
else:
	print("Cannot find a valid Takeout archive.")

# Begin traversal of extracted Takeout archive
if Path(os.path.join(takeout_dir, 'Takeout','Google Play Music')).is_dir():
	gpm_dir=os.path.join(takeout_dir, 'Takeout','Google Play Music')
	# Playlists
	if Path(os.path.join(gpm_dir, 'Playlists')).is_dir():
		# Initialize empty list for playlist dicts
		playlists_list = []
		# Import playlists to parse
		playlists = import_playlists(os.path.join(gpm_dir, 'Playlists'))
		# Begin to parse playlists
		for l in playlists:
			# Begin to parse playlist metadata
			# Initialize empty dict for playlist data
			playlist_data = {}
			# Check to make sure Metadata.csv exists and is a file
			metadata_file = os.path.join(l, 'Metadata.csv')
			if Path(metadata_file).is_file():
				playlist_data = parse_playlist_metadata(metadata_file)
				playlists_list.append(playlist_data)
			# End of parse playlist metadata
			# Begin to parse playlist track data
			track_dir = os.path.join(l, 'Tracks')
			if Path(track_dir).is_dir():
				track_files = glob.glob(os.path.join(track_dir, '*.csv'))
				for f in track_files:
					track_data = parse_track_data(f)
					playlists_list[-1]['data'].append(track_data)
				playlists_list[-1]['data'] = sorted(playlists_list[-1]['data'], key=itemgetter('playlist_index'))
		for l in playlists_list:
			print(json.dumps(l, indent=2))
		#print(json.dumps(playlists_list[-1], indent=2))
	# End of Playlists
	# Radio Stations									
	if Path(os.path.join(gpm_dir, 'Radio Stations')).is_dir():
		var='yes'
	# Tracks
	if Path(os.path.join(gpm_dir, 'Tracks')).is_dir():
		var='no'
# Make sure the Takeout archive contains 
### END OF APP