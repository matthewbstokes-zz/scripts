#!/bin/bash

avi=".avi"
for file in /home/user/XBoxShare/$1
do
  filename="${file%.*}"
  ffmpeg -i "$file" -vcodec libxvid -b 5017k -s hd720 -acodec libmp3lame -ab 128k -ac 2 "$filename$avi"
done
