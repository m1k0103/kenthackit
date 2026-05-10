#!/bin/bash

while getopts 's:h' opt; do
  case "$opt" in
    s)
      arg="$OPTARG"
      sshpass -p 'hackathonsuk' ssh student@192.168.137.1 -f "cd raspberrypi; echo '${OPTARG}' > forwarder.txt"
      
      ;;
   
    ?|h)
      echo "Usage: $(basename $0) [-s arg]"
      exit 1
      ;;
  esac
done
shift "$(($OPTIND -1))"

