## Script to update the thumbnail image in a .orbapreset file. The image supplied must be
## a 120px x 120px PNG image.
## Copyright (C) 2022 subskybox@gmail.com - All Rights Reserved
## Last revised 05/26/2022
##
## USAGE: ./OrbaUpdateThumbnail.ps1
##

$USAGE="USAGE: ./OrbaUpdateThumbnail.ps1 [orbapreset file] [png file]"

# Check if there are two parameters passed to the script
if ($args.length -lt 2) {
    Write-Host $USAGE
    Exit 1
}

# Create variables for the files
$orbapresetFile=$args[0]
$pngFile=$args[1]

# Test that the orbapreset file exists
if (-not(Test-Path -Path $orbapresetFile -PathType Leaf)) {
	Write-Host "ERROR: The orbapresetFile does not exist."
    Write-Host $USAGE
	Exit 1
}

# Test that the orbapreset file contains the target token
if (-not(Get-Content $orbapresetFile | Select-String -Pattern 'coverImage=').Matches.Success) {
  	Write-Host "ERROR: The orbapresetFile is not a valid orbapresetFile."
    Write-Host $USAGE
	Exit 1
}

# Test that the pngFile file exists
if (-not(Test-Path -Path $pngFile -PathType Leaf)) {
	Write-Host "ERROR: The pngFile does not exist."
    Write-Host $USAGE
	exit 1
}

$imageFormat=(Get-ChildItem $pngFile).Extension.ToString().ToLower()
# Test that the image file is a PNG 
if ( $imageFormat -ne ".png") {
  	Write-Host "ERROR: The image file must be a png image format."
    Write-Host $USAGE
	Exit 1
}

add-type -AssemblyName System.Drawing
$pngObj = New-Object System.Drawing.Bitmap $pngFile

# Test that the image file has the dimensions 120px x 120px 
if ( ($pngObj.Width -ne 120) -or ($pngObj.Height -ne 120) ) {
  	Write-Host "ERROR: The image file must have the dimentions 120px x 120px."
    Write-Host $USAGE
	exit 1
}

# Get the base64 encoded image and swap it into the orbapreset file.
$base64Str=[convert]::ToBase64String((Get-Content -path $pngFile -Encoding byte))
[regex]$pattern='coverImage="[^"]*"'
$newCoverImageStr = 'coverImage="' + $base64Str + '"'
$pattern.replace([IO.File]::ReadAllText($orbapresetFile),$newCoverImageStr,1) |
set-content $orbapresetFile

# Report Success
Write-Host "1 File was modified." -ForegroundColor Gray