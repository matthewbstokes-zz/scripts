#!/bin/bash

FOLDER_PATH=/home/user/Desktop/test
LOG_FILE=/home/user/Desktop/delete_movie.log
STORAGE_DAYS=30

# remove all spaces in filenames and replace with an underscore
find $folder -name "* *" -type f | rename 's/ /_/g'

# find all files in the folder path
find_file=`find $FOLDER_PATH \( -iname '*' -o -iname '.*' \) -type f`

for f in $find_file                           # loop through files in dir
do
  filename=`basename $f`                      # get just filename
  if [[ ${filename:0:1} != \. ]]              # NOT hidden file
  then                                    
    hidden_file=".$filename"
    hidden_file_path="$FOLDER_PATH$hidden_file"
    if [ -f $FOLDER_PATH$hidden_file ]        # check for hidden file
    then
      echo "Hidden File $hidden_file Found"   # check date in hidden file
      num=`cat $hidden_file_path`
      if [ $num == 0 ]
      then
        echo "Removing $STORAGE_DAYS Day Old File $filename"
        rm $f
        rm $hidden_file_path
        echo $LOG_FILE
        echo $filename >> $LOG_FILE
      else
        new_day=$((num - 1))
        echo "$num Days Left"
        echo $new_day > $hidden_file_path
      fi
    else
      # new file therefore create hidden doc
      echo "Creating Hidden Log File for $filename"        
      echo $STORAGE_DAYS > $hidden_file_path
      chmod 777 $hidden_file_path
      chmod 777 $f
    fi
  fi
done
