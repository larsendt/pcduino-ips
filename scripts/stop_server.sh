#!/bin/bash

pid=`pgrep -f "python ../api/pcduino_ips.py"`
if [ $pid ]
then
    echo "Killed $pid"
    kill $pid
else
    echo "No process to kill"
    exit 0
fi
