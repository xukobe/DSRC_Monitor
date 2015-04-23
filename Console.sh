#!/bin/sh

if [ $# -eq 0 ]
then
    echo "Not enough arguments!"
else
    if [ "$1" = "simulation" ]
        then
            python /etc/DSRC_Monitor/DSRC_Main/main.py simulation
    elif [ "$1" = "stationary" ]
        then
            python /etc/DSRC_Monitor/DSRC_Main/main.py stationary
    fi
fi


