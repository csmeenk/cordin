#!/bin/bash

# timestamp_file.sh
#
# Script to add time stamp values onto a .avi video.
#
# 	ARGUMENTS:
#		filename - the avi file
#		fps - number of frames/second
#		tstart - time of the first frame in seconds (can be positive or negative)
#
#	USAGE:
#		$ timestamp_file.sh 170208155837.avi 2000 -4e-3
#	To write stdout and stderr to a data file:
#		$ timestamp_file.sh 170208155837.avi 2000 -4e-3 1> log.txt 2> err.txt
#
# Christopher Smeenk 15.02.2017

#echo "Number of arguments= " $#

# check arguments
if [ $# = 4 ]; then
	filename=$1
	fps=$2
	tstart=$3
	magnification=$4
	
else
	echo "Error in `basename $0`"
	echo "Insufficient number of input arguments"
	exit
fi

# make a directory
dirname="${filename%.*}"
mkdir $dirname

# extract the frames from an avi file
mplayer $filename -vo jpeg:outdir=$dirname -ao null

# insert timestamps on each frame
cd $dirname
timestamp_ims_sh.py 00.jpg $fps $tstart $magnification


# Optionally write the images to an .avi movie using:
mencoder "mf://tstamp/*_tstamp.jpg" -mf fps=20 -o newanim.avi -ovc copy -lavcopts vcodec=msmpeg4v2
cd ..
