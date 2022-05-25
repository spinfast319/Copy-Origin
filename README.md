# Copy-Origin: Match Folder and Copy Gazelle-Origin Files
### A python script that loops through folder names in two specified directories. If it finds a match it copys the origin file from one to the other.

If you have more than one copy of all your albums, a back up folder for instance, this script lets you copy the origin files from one set of albums to the other.

This script recursively looks through all the album folders in a directory for for folders with origin.yaml files.  If a directory has one it then checks another directory you specify to see if there is a matching album. If there is one it checks if that album folder has an origin file. 
If there is one it replaces it with once from the directory you are starting with or just copies it over if the directory doesn't have one.  

It can handle albums with artwork folders or multiple disc folders in them. It can also handle specials characters and skips and logs any albums that have characters that makes windows fail. It has been tested and works in both Ubuntu Linux and Windows 10.

## Install and set up
Clone this script where you want to run it.

Set up or specify the three directories you will be using and specify whether you albums are nested under artist or not.
1. The directory of the albums that have up to date orgin files
2. The directory of albums that you want to update with new origin files
3. A directory to store the log files the script creates
4. Set the album_depth variable to specify whether you are using nested folders or have all albums in one directory
   - If you have all your ablums in one music directory, ie. Music/Album then set this value to 1
   - If you have all your albums nest in a Music/Artist/Album style of pattern set this value to 2

The default is 1 (Music/Album)

Then run the script from the command line.  It will output how many origin files it copied over as well as how many folders it looked for them in.

It will also create logs of any missing origin files it finds and save to the logs folder.
- Logs in the bad-missing-origin.txt file are folders that should have origin files and are missing them.
- Logs in the good-missing-origin.txt file are folders that probably should not have origin files. You can double-check these if you want.
