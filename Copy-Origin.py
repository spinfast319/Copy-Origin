#!/usr/bin/env python3

# Match Folder and Copy Gazelle-Origin Files
# author: hypermodified
# This script loops through folder names in two specified directories and copys and origin file from one to the other if it finds a match.
# It can handle albums with artwork folders or multiple disc folders in them. 
# It can also handle specials characters and skips and logs any characters that makes windows fail.
# It has been tested and works in both Ubuntu Linux and Windows 10.

# Import dependencies
import os  # Imports functionality that let's you interact with your operating system
import shutil # Imports functionality that lets you copy files and directory
import datetime # Imports functionality that lets you make timestamps
import re # Imports regex

#  Set your directories here
album_directory = "M:\Music" # Which directory do has origin files you want to copy?
copy_to_directory ="W:\RED-UL-Transmission-09\downloads\complete\_flac" # Which directory do you want to add or replace origin files with?
log_directory = "M:\Python Test Environment\Logs" # Which directory do you want the log in?

# Set whether you are using nested folders or have all albums in one directory here
# If you have all your ablums in one music directory Music/Album_name then set this value to 1
# If you have all your albums nest in a Music/Artist/Album style of pattern set this value to 2
# The default is 1
album_depth = 1

# Establishes the counters for completed albums and missing origin files
count = 0
loop_count = 0
good_missing = 0
bad_missing = 0
bad_folder_name = 0
error_message = 0

# identifies location origin files are supposed to be
path_segments = album_directory.split(os.sep)
segments = len(path_segments)
origin_location = segments + album_depth

#intro text
print("")
print("Double the flavor.")
print("")

# A function to log events
def log_outcomes(d,p,m):
    global log_directory
    script_name = "Copy-Origin Script"
    today = datetime.datetime.now()
    log_name = p
    directory = d
    message = m
    album_name = directory.split(os.sep)
    album_name = album_name[-1]
    log_path = log_directory + os.sep + log_name + ".txt"
    with open(log_path, 'a',encoding='utf-8') as log_name:
        log_name.write("--{:%b, %d %Y}".format(today)+ " at " +"{:%H:%M:%S}".format(today)+ " from the " + script_name + ".\n")
        log_name.write("The album folder " + album_name + " " + message + ".\n")
        log_name.write("Album location: " + directory + "\n")
        log_name.write(" \n")  
        log_name.close()
        
#  A function to identify folders with the same name and copy origin files from one to the other
def copy_origin(directory):
        global count
        global loop_count
        global good_missing
        global bad_missing
        global bad_folder_name
        global origin_location
        global copy_to_directory
        print ("\n")
        loop_count +=1 # variable will increment every loop iteration
        #check to see if folder has bad characters and skip if it does
        #get album name from directory
        re1 = re.compile(r"[\\/:*\"<>|?]");
        name_to_check = directory.split(os.sep)
        name_to_check = name_to_check[-1]
        if re1.search(name_to_check):
            print ("Illegal windows character detected.")
            print("--Logged album skipped due to illegal characters.")
            log_name = "illegal-characters"
            log_message = "was skipped due to illegal characters"
            log_outcomes(directory,log_name,log_message)
            bad_folder_name +=1 # variable will increment every loop iteration
            
        else:
            print("Checking for origin file in " + directory)
            #check to see if there is an origin file
            file_exists = os.path.exists('origin.yaml')
            if file_exists == True:
                print("--Origin file found for " + name_to_check)
                
                #check for matchting folder name in copy_to_directory
                print("Looking for the same directory as " + name_to_check)
                test_path_album = copy_to_directory + os.sep + name_to_check
                isdir_album = os.path.isdir(test_path_album)
                if isdir_album == True:
                    print("There is a matching album called " + name_to_check)
                    #check to see if there is an origin file
                    source_origin = directory  + os.sep + 'origin.yaml'
                    copy_origin = test_path_album + os.sep + 'origin.yaml'
                    other_file_exists = os.path.exists(copy_origin)
                    if other_file_exists == True:
                        print("--Origin file found for " + name_to_check)
                        #if an origin file exists delete it
                        os.remove(copy_origin)
                        print("--Origin file deleted")                        
                        #copy the origin from the source to the matching album
                        shutil.copy(source_origin, copy_origin)  
                        print ("--Origin file copied from source to match")
                        count +=1 # variable will increment every loop iteration
                    else:
                        print("No origin file in " + name_to_check)
                        #if no origin file exists copy from the source to the matching album
                        shutil.copy(source_origin, copy_origin)  
                        print ("--Origin file copied from source to match")
                        count +=1 # variable will increment every loop iteration
                else:
                    print("No matching album.")
                                                                 
            #otherwise log that the origin file is missing
            else:
                #split the directory to make sure that it distinguishes between folders that should and shouldn't have origin files
                current_path_segments = directory.split(os.sep)
                current_segments = len(current_path_segments)
                #create different log files depending on whether the origin file is missing somewhere it shouldn't be
                if origin_location != current_segments:
                    #log the missing origin file folders that are likely supposed to be missing
                    print ("--An origin file is missing from a folder that should not have one.")
                    print("--Logged missing origin file.")
                    log_name = "good-missing-origin"
                    log_message = "origin file is missing from a folder that should not have one.\nSince it shouldn't be there it is probably fine but you can double check"
                    log_outcomes(directory,log_name,log_message)
                    good_missing +=1 # variable will increment every loop iteration
                else:    
                    #log the missing origin file folders that are not likely supposed to be missing
                    print ("--An origin file is missing from a folder that should have one.")
                    print("--Logged missing origin file.")
                    log_name = "bad-missing-origin"
                    log_message = "origin file is missing from a folder that should have one"
                    log_outcomes(directory,log_name,log_message)
                    bad_missing +=1 # variable will increment every loop iteration
        
# Get all the subdirectories of album_directory recursively and store them in a list:
directories = [os.path.abspath(x[0]) for x in os.walk(album_directory)]
directories.remove(os.path.abspath(album_directory)) # If you don't want your main directory included

# Run a loop that goes into each directory identified and updates the origin file
for i in directories:
      os.chdir(i)         # Change working Directory
      copy_origin(i)      # Run your function
        
# Summary text
print("")
print("Double the fun. This script copied " + str(count) + " origin files out of "+ str(loop_count) + " albums looking for matches.")
print("This script looks for potential missing files or errors. The following messages outline whether any were found.")
if bad_folder_name >= 1:
    print("--Warning: There were " + str(bad_folder_name) + " folders with illegal characters.")
    error_message +=1 # variable will increment if statement is true
elif bad_folder_name == 0:    
    print("--Info: There were " + str(bad_folder_name) + " folders with illegal characters.")
if bad_missing >= 1:
    print("--Warning: There were " + str(bad_missing) + " folders missing an origin files that should have had them.")
    error_message +=1 # variable will increment if statement is true
elif bad_missing == 0:    
    print("--Info: There were " + str(bad_missing) + " folders missing an origin files that should have had them.")
if good_missing >= 1:
    print("--Info: Some folders didn't have origin files and probably shouldn't have origin files. " + str(good_missing) + " of these folders were identified.")
    error_message +=1 # variable will increment if statement is true
elif good_missing == 0:    
    print("--Info: Some folders didn't have origin files and probably shouldn't have origin files. " + str(good_missing) + " of these folders were identified.")
if error_message >= 1:
    print("Check the logs to see which folders had errors and what they were.")
else:
    print("There were no errors.")    
