#!python3.5

"""
rGREAT is the best if it works for you. But it doesn't work for me.

Motivation
----------

My work here at St. Jude is to develop pipelines and simplify user's effort for NGS analyses.
I don't want users, when finish running my HemTools pipeline, have to upload bed files to GREAT
server themselves.

Summary
-------

This tool uses Dropbox to create a sharable link and then use it for GREAT analysis. It will
print out a GREAT url. You then just need to copypaste the url to a browser to check out the results.


Installation
------------

module load conda3
conda create -n share_url
source activate share_url
conda install -c anaconda dropbox

Please follow the dropbox instruction below, mainly, you need a token.
The dropbox code is taken from: https://gist.github.com/Keshava11/d14db1e22765e8de2670b8976f3c7efb

Usage
-----

python pyGREAT.py test.bed

Return
------

http://great.stanford.edu/public/cgi-bin/greatStart.php?requestURL=https://www.dropbox.com/s/jd9q2489k91m8bj/test.bed?dl=0&requestSpecies=hg19&requestName=ensGene&requestSender=UCSC%20Table%20Browser

"""

# Prerequisites :
# 1.SetUp dropbox sdk to be able to use Dropbox Api's
# $ sudo pip install dropbox
# By default python dropbox sdk is based upon the python 3.5
#
# 2. Create an App on dropbox console (https://www.dropbox.com/developers/apps) which will be used and validated to do
# the file upload and restore using dropbox api. Mostly you need an access token to connect to Dropbox before actual file/folder operations.
#
# 3. Once done with code, run the script by following command
# $ python SFileUploader.py // if python3.5 is default


import sys
import dropbox

from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError

# Access token
TOKEN = ''

LOCALFILE = sys.argv[1]
BACKUPPATH = '/%s'%(sys.argv[1]) # Keep the forward slash before destination filename


# Uploads contents of LOCALFILE to Dropbox
def backup():
	with open(LOCALFILE, 'rb') as f:
		# We use WriteMode=overwrite to make sure that the settings in the file
		# are changed on upload
		print("Uploading " + LOCALFILE + " to Dropbox as " + BACKUPPATH + "...")
		try:
			dbx.files_upload(f.read(), BACKUPPATH, mode=WriteMode('overwrite'))
		except ApiError as err:
			# This checks for the specific error where a user doesn't have enough Dropbox space quota to upload this file
			if (err.error.is_path() and
					err.error.get_path().error.is_insufficient_space()):
				sys.exit("ERROR: Cannot back up; insufficient space.")
			elif err.user_message_text:
				print(err.user_message_text)
				sys.exit()
			else:
				print(err)
				sys.exit()


# Adding few functions to check file details
def checkFileDetails():
	print("Checking file details")

	for entry in dbx.files_list_folder('').entries:
		print("File list is : ")
		print(entry.name)


# Run this script independently
if __name__ == '__main__':
	# Check for an access token
	if (len(TOKEN) == 0):
		sys.exit("ERROR: Looks like you didn't add your access token. Open up backup-and-restore-example.py in a text editor and paste in your token in line 14.")

	# Create an instance of a Dropbox class, which can make requests to the API.
	print("Creating a Dropbox object...")
	dbx = dropbox.Dropbox(TOKEN)

	# Check that the access token is valid
	try:
		dbx.users_get_current_account()
	except AuthError as err:
		sys.exit(
			"ERROR: Invalid access token; try re-generating an access token from the app console on the web.")

	try:
		checkFileDetails()
	except Error as err:
		sys.exit("Error while checking file details")

	print("Creating backup...")
	# Create a backup of the current settings file
	backup()

	print("Done!")
	
	result = dbx.sharing_create_shared_link_with_settings(BACKUPPATH).url
	
	print (result)
	
	print ("http://great.stanford.edu/public/cgi-bin/greatStart.php?requestURL=%s&requestSpecies=hg19&requestName=ensGene&requestSender=UCSC%20Table%20Browser"%(result))