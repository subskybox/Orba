#!/bin/sh
## Script to update Disentangle.orbapreset with a new ModifierData string
## from the clipboard. It then renames the file to force the Orba App to update.
## Copyright (C) 2022 subskybox@gmail.com - All Rights Reserved
## Last revised 06/01/2022
##
## USAGE: ./OrbaDeployDaemon.sh
##

echo "Listening..."

# Check every second for the DEPLOY token in the clipboard
while :; do
    sleep 1
    modifierData=$(pbpaste)
    if  [[ $modifierData == DEPLOY* ]] && [ ${#modifierData} -eq 242 ] ; then

    	echo "Deploying..."

    	# Trim the token from the clipboard to prevent redeployment
		modifierData=${modifierData:6}
		echo $modifierData | pbcopy

    	# Change directory to the Orba Chords folder
		cd ~/Library/Artiphon/Orba/Presets/Chords/

		# Create the file Disentangle.orbapreset if it doesn't exist
		FILE=~/Library/Artiphon/Orba/Presets/Chords/Disentangle.orbapreset
		if ! test -f "$FILE"; then
		    cp 1981.orbapreset Disentangle.orbapreset
		fi

		# If the clipboard contains a new modifierData string
		# Replace the old modifierData string with the new one (from the clipboard)
		if [ ${#modifierData} -eq 236 ]; then
			perl -pi -w -e '!$x && s{modifierData="[^"]*}{modifierData="'$modifierData'} && ($x=1)' Disentangle.orbapreset
		fi

		# Rename Disentangle.orbapreset twice to force the Orba App to pickup the change
		mv Disentangle.orbapreset tmp.tmp
		sleep 2
		mv tmp.tmp Disentangle.orbapreset
		sleep 2
		echo $(date)
		GREEN='\033[0;32m'
		BLUE='\033[0;34m' 
		NC='\033[0m' # No Color
		printf " ${GREEN}Deployed${NC} - Load ${BLUE}Disentangle${NC} voice from the Orba Chord Presets.\n"
		open -a "Orba"
	fi
done