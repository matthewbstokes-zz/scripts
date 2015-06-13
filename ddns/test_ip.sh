#!/bin/bash
# Get external IP address

output_file=/home/user/Dropbox/ip.txt

current_ip=$(curl http://mire.ipadsl.net | sed -nr -e 's|^.*<span class="ip">([0-9.]+)</span>.*$|\1| p')
echo "IP: $current_ip"

prev_ip=$(cat /home/user/Dropbox/ip.txt)
echo "Previous IP: $prev_ip"

if [[ $current_ip != $prev_ip ]]
then
  echo $current_ip > $output_file
  echo "New IP Saved"
fi
