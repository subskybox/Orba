#!/bin/sh
## Script to update the thumbnail image in a .orbapreset file. The image supplied must be
## a 120px x 120px PNG image.
## Copyright (C) 2022 subskybox@gmail.com - All Rights Reserved
## Last revised 05/25/2022
##
## USAGE: ./OrbaUpdateThumbnail.sh [orbapreset file] [png file]
##
	
USAGE="USAGE: ./OrbaUpdateThumbnail.sh [orbapreset file] [png file]"

# Check if there are two parameters passed to the script
if [ $# -lt 2 ]; then
	echo "USAGE: ./OrbaUpdateThumbnail.sh [orbapreset file] [png file]"
	exit 1
fi

# Create variables for the files
orbapresetFile=$1
pngFile=$2

# Test that the orbapreset file exists
if ! test -f "$orbapresetFile"; then
	echo "ERROR: The orbapresetFile does not exist."
    echo $USAGE
	exit 1
fi

# Test that the orbapreset file contains the target token
if ! grep -q "coverImage=" "$orbapresetFile"; then
  	echo "ERROR: The orbapresetFile is not a valid orbapresetFile."
    echo $USAGE
	exit 1
fi

# Test that the pngFile file exists
if ! test -f "$pngFile"; then
	echo "ERROR: The pngFile does not exist."
    echo $USAGE
	exit 1
fi

imageFormat=$(file -b $pngFile | cut -f 1 -d ",")
imageDimensions=$(file -b $pngFile | cut -f 2 -d ",")

# Test that the image file is a PNG 
if [ "$imageFormat" != "PNG image data" ]; then
  	echo "ERROR: The image file must be a png image format."
    echo $USAGE
	exit 1
fi

# Test that the image file has the dimensions 120px x 120px 
if [ "$imageDimensions" != " 120 x 120" ]; then
  	echo "ERROR: The image file must have the dimentions 120px x 120px."
    echo $USAGE
	exit 1
fi

# Get the base64 encoded image and swap it into the orbapreset file.
base64Str=$(base64 $pngFile)
perl -pi -w -e 's{coverImage="[^"]*}{coverImage="'$base64Str'}' $orbapresetFile

# Report Success
GREEN='\033[0;32m'
printf " ${GREEN}1 File was modified.${NC}.\n"
#open -a "Orba"